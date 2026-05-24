from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

DAY_KEYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
PERSON_DEFS = [
    ('drake', 'Drake', 'VP Operations', 'Leadership', None),
    ('ricardo', 'Ricardo', 'Milwaukee operations manager', 'Milwaukee', 'drake'),
    ('norman', 'Norman', 'Salt Lake City operations manager', 'Salt Lake City', 'drake'),
    ('cody', 'Kody', 'Milwaukee outbound manager', 'Milwaukee Outbound', 'ricardo'),
    ('hugh', 'Hugh', 'Milwaukee second shift manager', 'Milwaukee 2nd Shift', 'ricardo'),
    ('luis', 'Luis', 'Milwaukee inventory manager', 'Milwaukee Inventory', 'ricardo'),
    ('adam', 'Adam', 'Milwaukee special projects / B2B manager', 'Milwaukee Special Projects / B2B', 'ricardo'),
    ('emily', 'Emily', 'Milwaukee inbound / returns manager', 'Milwaukee Inbound / Returns', 'ricardo'),
    ('danielle', 'Yaniel', 'Shipping coordinator', 'Night shift', 'cody'),
    ('ana', 'Anna', 'Packing lead', 'Night shift', 'cody'),
    ('remar', 'Ramar', 'Unload lead', 'Night shift', 'luis'),
    ('brenda', 'Brenda', 'Receiving lead', 'Night shift', 'luis'),
    ('nate', 'Nate', 'Floor lead', 'Closing shift', 'adam'),
    ('maria', 'Maria', 'Inventory control', 'Swing shift', 'adam'),
    ('edwin', 'Edwin', 'Cycle count lead', 'Swing shift', 'adam'),
    ('rely', 'Rely', 'Returns coordinator', 'Closing shift', 'emily'),
    ('santana', 'Santana', 'Project coordinator', 'Day shift', 'norman'),
]

SECTION_DEFS = [
    ('milwaukee-rollup', 'Milwaukee roll-up', 'ricardo', 'Milwaukee', 'city'),
    ('milwaukee-outbound', 'Milwaukee Outbound', 'cody', 'Milwaukee', 'function'),
    ('milwaukee-inventory', 'Milwaukee Inventory', 'luis', 'Milwaukee', 'function'),
    ('milwaukee-inbound-returns', 'Milwaukee Inbound / Returns', 'emily', 'Milwaukee', 'function'),
    ('milwaukee-second-shift', 'Milwaukee 2nd Shift', 'hugh', 'Milwaukee', 'function'),
    ('milwaukee-special-projects-b2b', 'Milwaukee Special Projects / B2B', 'adam', 'Milwaukee', 'function'),
    ('salt-lake-city-operations', 'Salt Lake City Operations', 'norman', 'Salt Lake City', 'city'),
]


@dataclass(frozen=True)
class LeadershipSection:
    id: str
    label: str
    owner_person_id: str
    location: str
    kind: str


@dataclass(frozen=True)
class Question:
    id: str
    type: str
    source: str
    prompt: str
    helper: str = ''
    placeholder: str = ''
    choices: list[str] = field(default_factory=list)
    cadence: str | None = None
    days: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Person:
    id: str
    name: str
    role: str
    team: str
    manager_id: str | None
    can_assign: bool
    default_questions: list[Question]


@dataclass(frozen=True)
class ReportAnswerInput:
    question_key: str
    question_text: str
    answer_value: str
    answer_type: str
    source: str


@dataclass(frozen=True)
class ReportInput:
    person_id: str
    report_date: date
    answers: list[ReportAnswerInput]
    summary_text: str = ''
    status: str = 'submitted'


@dataclass(frozen=True)
class QuestionAssignmentInput:
    created_by_person_id: str
    assigned_to_person_id: str
    prompt: str
    answer_type: str
    helper_text: str = ''
    placeholder: str = ''
    options: list[str] = field(default_factory=list)
    cadence: str = 'today'
    days: list[str] = field(default_factory=list)
    active: bool = True


@dataclass(frozen=True)
class ReportAnswerRecord:
    question_key: str
    question_text: str
    answer_value: str
    answer_type: str
    source: str


@dataclass(frozen=True)
class ReportRecord:
    id: int
    person_id: str
    report_date: date
    submitted_at: datetime
    status: str
    summary_text: str
    answers: list[ReportAnswerRecord]


@dataclass(frozen=True)
class QuestionAssignmentRecord:
    id: int
    created_by_person_id: str
    assigned_to_person_id: str
    prompt: str
    answer_type: str
    helper_text: str
    placeholder: str
    options: list[str]
    cadence: str
    days: list[str]
    active: bool
    created_at: datetime


def first_name(name: str) -> str:
    return name.split(' ')[0]


def default_questions_for(person_id: str, name: str) -> list[Question]:
    short_name = first_name(name)
    return [
        Question(
            id=f'{person_id}-mood',
            type='choice',
            source='default',
            prompt=f'How are we doing, {short_name}?',
            helper='Pick the closest fit.',
            choices=['Great', 'Good', 'Okay', 'Rough'],
        ),
        Question(
            id=f'{person_id}-wins',
            type='textarea',
            source='default',
            prompt='What is the biggest thing that went right on your side today?',
            helper='Short and useful beats long and perfect.',
            placeholder='Example: dock cleared before cutoff',
        ),
        Question(
            id=f'{person_id}-top3',
            type='textarea',
            source='default',
            prompt='What are your top 3 priorities for tomorrow?',
            helper='Use 3 short bullets or numbered lines.',
            placeholder='1. Approve temp labor\n2. Clear backlog\n3. Watch late carrier window',
        ),
        Question(
            id=f'{person_id}-risk',
            type='text',
            source='default',
            prompt='What is the one thing leadership should watch tomorrow?',
            helper='Give the cleanest handoff note you can.',
            placeholder='Example: labor gap in picking after 3 PM',
        ),
    ]


_children_by_manager: dict[str, list[str]] = {}
for person_id, _name, _role, _team, manager_id in PERSON_DEFS:
    _children_by_manager.setdefault(person_id, [])
    if manager_id:
        _children_by_manager.setdefault(manager_id, []).append(person_id)


PEOPLE: list[Person] = [
    Person(
        id=person_id,
        name=name,
        role=role,
        team=team,
        manager_id=manager_id,
        can_assign=person_id in {'drake', 'ricardo', 'norman', 'cody', 'luis', 'adam', 'emily'},
        default_questions=default_questions_for(person_id, name),
    )
    for person_id, name, role, team, manager_id in PERSON_DEFS
]

LEADERSHIP_SECTIONS: list[LeadershipSection] = [
    LeadershipSection(
        id=section_id,
        label=label,
        owner_person_id=owner_person_id,
        location=location,
        kind=kind,
    )
    for section_id, label, owner_person_id, location, kind in SECTION_DEFS
]
