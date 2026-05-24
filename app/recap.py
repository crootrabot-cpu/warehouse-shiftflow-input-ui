from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.models import Person, ReportAnswerRecord, ReportRecord


@dataclass(frozen=True)
class RecapItem:
    person: Person
    report: ReportRecord
    risk_answer: ReportAnswerRecord | None
    assigned_answers: list[ReportAnswerRecord]


@dataclass(frozen=True)
class RecapView:
    report_day: date
    submitted: list[RecapItem]
    missing: list[Person]
    top_wins: list[RecapItem]
    top_risks: list[tuple[Person, ReportAnswerRecord]]
    assigned_follow_ups: list[tuple[Person, ReportAnswerRecord]]


def build_recap(report_day: date, people: list[Person], reports: list[ReportRecord]) -> RecapView:
    people_by_id = {person.id: person for person in people}
    submitted_items: list[RecapItem] = []

    for report in reports:
        person = people_by_id[report.person_id]
        risk_answer = next((answer for answer in report.answers if answer.question_key.endswith('-risk')), None)
        assigned_answers = [
            answer
            for answer in report.answers
            if answer.source == 'manager-assigned' and answer.answer_value.strip()
        ]
        submitted_items.append(
            RecapItem(
                person=person,
                report=report,
                risk_answer=risk_answer,
                assigned_answers=assigned_answers,
            )
        )

    submitted_ids = {item.person.id for item in submitted_items}
    missing = [person for person in people if person.id not in submitted_ids]
    top_wins = [item for item in submitted_items if item.report.summary_text.strip()]
    top_risks = [
        (item.person, item.risk_answer)
        for item in submitted_items
        if item.risk_answer is not None and item.risk_answer.answer_value.strip()
    ]
    assigned_follow_ups = [
        (item.person, answer)
        for item in submitted_items
        for answer in item.assigned_answers
    ]

    return RecapView(
        report_day=report_day,
        submitted=submitted_items,
        missing=missing,
        top_wins=top_wins,
        top_risks=top_risks,
        assigned_follow_ups=assigned_follow_ups,
    )
