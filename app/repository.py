from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from app.db import connect, init_schema as init_db_schema
from app.models import (
    DAY_KEYS,
    PEOPLE,
    Person,
    Question,
    QuestionAssignmentInput,
    QuestionAssignmentRecord,
    ReportAnswerInput,
    ReportAnswerRecord,
    ReportInput,
    ReportRecord,
)

WEEKDAY_KEYS = {'mon', 'tue', 'wed', 'thu', 'fri'}
FULL_ORG_ASSIGNERS = {'drake', 'ricardo', 'norman'}


class SQLiteRepository:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)

    def init_schema(self) -> None:
        with connect(self.db_path) as connection:
            init_db_schema(connection)
            connection.executemany(
                '''
                INSERT INTO people (id, name, role, team, manager_id, can_assign)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name,
                    role=excluded.role,
                    team=excluded.team,
                    manager_id=excluded.manager_id,
                    can_assign=excluded.can_assign
                ''',
                [
                    (person.id, person.name, person.role, person.team, person.manager_id, int(person.can_assign))
                    for person in PEOPLE
                ],
            )
            connection.execute(
                'DELETE FROM people WHERE id NOT IN ({})'.format(', '.join('?' for _ in PEOPLE)),
                [person.id for person in PEOPLE],
            )
            connection.commit()

    def list_people(self) -> list[Person]:
        with connect(self.db_path) as connection:
            rows = connection.execute(
                'SELECT id, name, role, team, manager_id, can_assign FROM people ORDER BY rowid'
            ).fetchall()
        default_questions_by_id = {person.id: person.default_questions for person in PEOPLE}
        return [
            Person(
                id=row['id'],
                name=row['name'],
                role=row['role'],
                team=row['team'],
                manager_id=row['manager_id'],
                can_assign=bool(row['can_assign']),
                default_questions=default_questions_by_id[row['id']],
            )
            for row in rows
        ]

    def get_person(self, person_id: str) -> Person | None:
        for person in self.list_people():
            if person.id == person_id:
                return person
        return None

    def get_assignable_people(self, person_id: str) -> list[Person]:
        people = self.list_people()
        people_by_id = {person.id: person for person in people}
        manager = people_by_id.get(person_id)
        if manager is None or not manager.can_assign:
            return []

        if person_id in FULL_ORG_ASSIGNERS:
            return people

        children_by_manager: dict[str, list[str]] = {}
        for person in people:
            children_by_manager.setdefault(person.id, [])
            if person.manager_id:
                children_by_manager.setdefault(person.manager_id, []).append(person.id)

        allowed_ids: list[str] = []
        queue = list(children_by_manager.get(person_id, []))
        while queue:
            current = queue.pop(0)
            allowed_ids.append(current)
            queue.extend(children_by_manager.get(current, []))

        return [people_by_id[current_id] for current_id in allowed_ids]

    def save_report(self, report: ReportInput) -> ReportRecord:
        submitted_at = datetime.utcnow()
        with connect(self.db_path) as connection:
            cursor = connection.execute(
                '''
                INSERT INTO reports (person_id, report_date, submitted_at, status, summary_text)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (
                    report.person_id,
                    report.report_date.isoformat(),
                    submitted_at.isoformat(),
                    report.status,
                    report.summary_text,
                ),
            )
            report_id = cursor.lastrowid
            connection.executemany(
                '''
                INSERT INTO report_answers (
                    report_id, question_key, question_text, answer_value, answer_type, source
                ) VALUES (?, ?, ?, ?, ?, ?)
                ''',
                [
                    (
                        report_id,
                        answer.question_key,
                        answer.question_text,
                        answer.answer_value,
                        answer.answer_type,
                        answer.source,
                    )
                    for answer in report.answers
                ],
            )
            connection.commit()
        return ReportRecord(
            id=report_id,
            person_id=report.person_id,
            report_date=report.report_date,
            submitted_at=submitted_at,
            status=report.status,
            summary_text=report.summary_text,
            answers=[
                ReportAnswerRecord(
                    question_key=answer.question_key,
                    question_text=answer.question_text,
                    answer_value=answer.answer_value,
                    answer_type=answer.answer_type,
                    source=answer.source,
                )
                for answer in report.answers
            ],
        )

    def list_reports_for_day(self, report_day: date) -> list[ReportRecord]:
        with connect(self.db_path) as connection:
            report_rows = connection.execute(
                '''
                SELECT id, person_id, report_date, submitted_at, status, summary_text
                FROM reports
                WHERE report_date = ?
                ORDER BY submitted_at ASC, id ASC
                ''',
                (report_day.isoformat(),),
            ).fetchall()
            answer_rows = connection.execute(
                '''
                SELECT report_id, question_key, question_text, answer_value, answer_type, source
                FROM report_answers
                WHERE report_id IN (
                    SELECT id FROM reports WHERE report_date = ?
                )
                ORDER BY id ASC
                ''',
                (report_day.isoformat(),),
            ).fetchall()

        answers_by_report: dict[int, list[ReportAnswerRecord]] = {}
        for row in answer_rows:
            answers_by_report.setdefault(row['report_id'], []).append(
                ReportAnswerRecord(
                    question_key=row['question_key'],
                    question_text=row['question_text'],
                    answer_value=row['answer_value'],
                    answer_type=row['answer_type'],
                    source=row['source'],
                )
            )

        return [
            ReportRecord(
                id=row['id'],
                person_id=row['person_id'],
                report_date=date.fromisoformat(row['report_date']),
                submitted_at=datetime.fromisoformat(row['submitted_at']),
                status=row['status'],
                summary_text=row['summary_text'],
                answers=answers_by_report.get(row['id'], []),
            )
            for row in report_rows
        ]

    def get_report(self, report_id: int) -> ReportRecord | None:
        with connect(self.db_path) as connection:
            report_row = connection.execute(
                '''
                SELECT id, person_id, report_date, submitted_at, status, summary_text
                FROM reports
                WHERE id = ?
                ''',
                (report_id,),
            ).fetchone()
            if report_row is None:
                return None
            answer_rows = connection.execute(
                '''
                SELECT question_key, question_text, answer_value, answer_type, source
                FROM report_answers
                WHERE report_id = ?
                ORDER BY id ASC
                ''',
                (report_id,),
            ).fetchall()

        return ReportRecord(
            id=report_row['id'],
            person_id=report_row['person_id'],
            report_date=date.fromisoformat(report_row['report_date']),
            submitted_at=datetime.fromisoformat(report_row['submitted_at']),
            status=report_row['status'],
            summary_text=report_row['summary_text'],
            answers=[
                ReportAnswerRecord(
                    question_key=row['question_key'],
                    question_text=row['question_text'],
                    answer_value=row['answer_value'],
                    answer_type=row['answer_type'],
                    source=row['source'],
                )
                for row in answer_rows
            ],
        )

    def save_assignment(self, assignment: QuestionAssignmentInput) -> QuestionAssignmentRecord:
        created_at = datetime.utcnow()
        with connect(self.db_path) as connection:
            cursor = connection.execute(
                '''
                INSERT INTO question_assignments (
                    created_by_person_id,
                    assigned_to_person_id,
                    prompt,
                    answer_type,
                    helper_text,
                    placeholder,
                    options_json,
                    cadence,
                    days_json,
                    active,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    assignment.created_by_person_id,
                    assignment.assigned_to_person_id,
                    assignment.prompt,
                    assignment.answer_type,
                    assignment.helper_text,
                    assignment.placeholder,
                    json.dumps(assignment.options),
                    assignment.cadence,
                    json.dumps(_normalize_days(assignment.days, assignment.cadence)),
                    int(assignment.active),
                    created_at.isoformat(),
                ),
            )
            assignment_id = cursor.lastrowid
            connection.commit()
        return QuestionAssignmentRecord(
            id=assignment_id,
            created_by_person_id=assignment.created_by_person_id,
            assigned_to_person_id=assignment.assigned_to_person_id,
            prompt=assignment.prompt,
            answer_type=assignment.answer_type,
            helper_text=assignment.helper_text,
            placeholder=assignment.placeholder,
            options=assignment.options,
            cadence=assignment.cadence,
            days=_normalize_days(assignment.days, assignment.cadence),
            active=assignment.active,
            created_at=created_at,
        )

    def list_assignments_for_person(self, person_id: str) -> list[QuestionAssignmentRecord]:
        with connect(self.db_path) as connection:
            rows = connection.execute(
                '''
                SELECT
                    id,
                    created_by_person_id,
                    assigned_to_person_id,
                    prompt,
                    answer_type,
                    helper_text,
                    placeholder,
                    options_json,
                    cadence,
                    days_json,
                    active,
                    created_at
                FROM question_assignments
                WHERE assigned_to_person_id = ?
                ORDER BY id ASC
                ''',
                (person_id,),
            ).fetchall()
        return [_assignment_from_row(row) for row in rows]

    def list_assignments_created_by_person(self, person_id: str) -> list[QuestionAssignmentRecord]:
        with connect(self.db_path) as connection:
            rows = connection.execute(
                '''
                SELECT
                    id,
                    created_by_person_id,
                    assigned_to_person_id,
                    prompt,
                    answer_type,
                    helper_text,
                    placeholder,
                    options_json,
                    cadence,
                    days_json,
                    active,
                    created_at
                FROM question_assignments
                WHERE created_by_person_id = ?
                ORDER BY id DESC
                ''',
                (person_id,),
            ).fetchall()
        return [_assignment_from_row(row) for row in rows]

    def get_assignment(self, assignment_id: int) -> QuestionAssignmentRecord | None:
        with connect(self.db_path) as connection:
            row = connection.execute(
                '''
                SELECT
                    id,
                    created_by_person_id,
                    assigned_to_person_id,
                    prompt,
                    answer_type,
                    helper_text,
                    placeholder,
                    options_json,
                    cadence,
                    days_json,
                    active,
                    created_at
                FROM question_assignments
                WHERE id = ?
                ''',
                (assignment_id,),
            ).fetchone()
        if row is None:
            return None
        return _assignment_from_row(row)

    def update_assignment(
        self,
        assignment_id: int,
        created_by_person_id: str,
        assigned_to_person_id: str,
        prompt: str,
        answer_type: str,
        helper_text: str,
        cadence: str,
    ) -> QuestionAssignmentRecord:
        existing = self.get_assignment(assignment_id)
        if existing is None:
            raise ValueError(f'Assignment {assignment_id} not found')
        normalized_days = _normalize_days(existing.days, cadence)
        with connect(self.db_path) as connection:
            connection.execute(
                '''
                UPDATE question_assignments
                SET created_by_person_id = ?,
                    assigned_to_person_id = ?,
                    prompt = ?,
                    answer_type = ?,
                    helper_text = ?,
                    cadence = ?,
                    days_json = ?
                WHERE id = ?
                ''',
                (
                    created_by_person_id,
                    assigned_to_person_id,
                    prompt,
                    answer_type,
                    helper_text,
                    cadence,
                    json.dumps(normalized_days),
                    assignment_id,
                ),
            )
            connection.commit()
        updated = self.get_assignment(assignment_id)
        if updated is None:
            raise ValueError(f'Assignment {assignment_id} not found after update')
        return updated

    def set_assignment_active(self, assignment_id: int, active: bool) -> QuestionAssignmentRecord:
        with connect(self.db_path) as connection:
            connection.execute(
                'UPDATE question_assignments SET active = ? WHERE id = ?',
                (int(active), assignment_id),
            )
            connection.commit()
        updated = self.get_assignment(assignment_id)
        if updated is None:
            raise ValueError(f'Assignment {assignment_id} not found after active toggle')
        return updated

    def get_questions_for_person(self, person_id: str, on_date: date) -> list[Question]:
        people_by_id = {person.id: person for person in PEOPLE}
        person = people_by_id[person_id]
        assignments = [
            assignment
            for assignment in self.list_assignments_for_person(person_id)
            if _assignment_applies_on_date(assignment, on_date)
        ]
        return person.default_questions + [
            Question(
                id=f'assignment-{assignment.id}',
                type=assignment.answer_type,
                source='manager-assigned',
                prompt=assignment.prompt,
                helper=assignment.helper_text,
                placeholder=assignment.placeholder,
                choices=assignment.options if assignment.answer_type in {'choice', 'multi-select'} else [],
                cadence=assignment.cadence,
                days=assignment.days,
            )
            for assignment in assignments
        ]


def _assignment_from_row(row) -> QuestionAssignmentRecord:
    return QuestionAssignmentRecord(
        id=row['id'],
        created_by_person_id=row['created_by_person_id'],
        assigned_to_person_id=row['assigned_to_person_id'],
        prompt=row['prompt'],
        answer_type=row['answer_type'],
        helper_text=row['helper_text'],
        placeholder=row['placeholder'],
        options=json.loads(row['options_json']),
        cadence=row['cadence'],
        days=json.loads(row['days_json']),
        active=bool(row['active']),
        created_at=datetime.fromisoformat(row['created_at']),
    )


def _normalize_days(days: list[str], cadence: str) -> list[str]:
    normalized = []
    for day in days:
        candidate = str(day).strip().lower()
        if candidate in DAY_KEYS and candidate not in normalized:
            normalized.append(candidate)
    if normalized:
        return normalized
    if cadence == 'weekdays':
        return sorted(WEEKDAY_KEYS, key=DAY_KEYS.index)
    return []


def _assignment_applies_on_date(assignment: QuestionAssignmentRecord, on_date: date) -> bool:
    if not assignment.active:
        return False
    day_key = DAY_KEYS[(on_date.weekday() + 1) % 7]
    if assignment.cadence in {'today', 'daily'}:
        return True
    if assignment.cadence == 'weekdays':
        return day_key in WEEKDAY_KEYS
    if assignment.cadence == 'custom':
        return day_key in assignment.days
    return True
