from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.models import Person, ReportAnswerRecord, ReportRecord


@dataclass(frozen=True)
class MetricCard:
    label: str
    value: str


@dataclass(frozen=True)
class RecapItem:
    person: Person
    report: ReportRecord
    risk_answer: ReportAnswerRecord | None
    assigned_answers: list[ReportAnswerRecord]
    summary_line: str


@dataclass(frozen=True)
class RecapView:
    report_day: date
    submitted: list[RecapItem]
    missing: list[Person]
    top_wins: list[RecapItem]
    top_risks: list[tuple[Person, ReportAnswerRecord]]
    assigned_follow_ups: list[tuple[Person, ReportAnswerRecord]]
    metric_cards: list[MetricCard]
    email_subject: str
    email_body: str


METRIC_SUFFIXES = {
    'labor_hours_spent': '-yesterday-labor-hours-spent',
    'hours_worked': '-yesterday-hours-worked',
    'orders_shipped': '-yesterday-orders-shipped',
    'units_per_hour': '-yesterday-units-per-hour',
    'cost_per_order': '-yesterday-cost-per-order',
    'orders_missed_sla': '-yesterday-orders-missed-sla',
}


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
                summary_line=_build_summary_line(person, report, risk_answer),
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
    metric_cards = _build_metric_cards(reports)
    email_subject = f'End-of-day recap for {report_day.isoformat()}'
    email_body = _build_email_body(
        report_day=report_day,
        metric_cards=metric_cards,
        submitted_items=submitted_items,
        top_risks=top_risks,
        assigned_follow_ups=assigned_follow_ups,
        missing=missing,
    )

    return RecapView(
        report_day=report_day,
        submitted=submitted_items,
        missing=missing,
        top_wins=top_wins,
        top_risks=top_risks,
        assigned_follow_ups=assigned_follow_ups,
        metric_cards=metric_cards,
        email_subject=email_subject,
        email_body=email_body,
    )


def _build_metric_cards(reports: list[ReportRecord]) -> list[MetricCard]:
    labor_hours_spent = _sum_metric(reports, METRIC_SUFFIXES['labor_hours_spent'])
    hours_worked = _sum_metric(reports, METRIC_SUFFIXES['hours_worked'])
    orders_shipped = _sum_metric(reports, METRIC_SUFFIXES['orders_shipped'])
    orders_missed_sla = _sum_metric(reports, METRIC_SUFFIXES['orders_missed_sla'])
    units_per_hour = _weighted_average_metric(
        reports,
        value_suffix=METRIC_SUFFIXES['units_per_hour'],
        weight_suffix=METRIC_SUFFIXES['hours_worked'],
    )
    cost_per_order = _weighted_average_metric(
        reports,
        value_suffix=METRIC_SUFFIXES['cost_per_order'],
        weight_suffix=METRIC_SUFFIXES['orders_shipped'],
    )

    return [
        MetricCard("Yesterday's labor hours spent", _format_number(labor_hours_spent, 1)),
        MetricCard("Yesterday's hours worked", _format_number(hours_worked, 1)),
        MetricCard("Yesterday's orders shipped", _format_number(orders_shipped, 0)),
        MetricCard("Yesterday's units per hour", _format_number(units_per_hour, 1)),
        MetricCard("Yesterday's cost per order", _format_number(cost_per_order, 2)),
        MetricCard("Yesterday's orders that missed SLA", _format_number(orders_missed_sla, 0)),
    ]


def _sum_metric(reports: list[ReportRecord], suffix: str) -> float | None:
    values = [_parse_number(answer.answer_value) for report in reports for answer in report.answers if answer.question_key.endswith(suffix)]
    numeric_values = [value for value in values if value is not None]
    if not numeric_values:
        return None
    return sum(numeric_values)


def _weighted_average_metric(reports: list[ReportRecord], value_suffix: str, weight_suffix: str) -> float | None:
    weighted_total = 0.0
    total_weight = 0.0
    fallback_values: list[float] = []
    for report in reports:
        value = _metric_value(report, value_suffix)
        if value is None:
            continue
        fallback_values.append(value)
        weight = _metric_value(report, weight_suffix)
        if weight is None or weight <= 0:
            continue
        weighted_total += value * weight
        total_weight += weight
    if total_weight > 0:
        return weighted_total / total_weight
    if fallback_values:
        return sum(fallback_values) / len(fallback_values)
    return None


def _metric_value(report: ReportRecord, suffix: str) -> float | None:
    answer = next((answer for answer in report.answers if answer.question_key.endswith(suffix)), None)
    if answer is None:
        return None
    return _parse_number(answer.answer_value)


def _parse_number(raw: str) -> float | None:
    cleaned = str(raw).strip().replace(',', '')
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def _format_number(value: float | None, decimals: int) -> str:
    if value is None:
        return '—'
    if decimals == 0:
        return f'{int(round(value)):,}'
    return f'{value:,.{decimals}f}'


def _build_summary_line(person: Person, report: ReportRecord, risk_answer: ReportAnswerRecord | None) -> str:
    summary = (report.summary_text or '').strip()
    if summary:
        sentence = f'{person.name} reported {_normalize_sentence(summary)}'
    else:
        sentence = f'{person.name} submitted an update without a clear win summary.'
    if risk_answer and risk_answer.answer_value.strip():
        sentence += f' Leadership should watch {_normalize_sentence(risk_answer.answer_value)}'
    return sentence


def _normalize_sentence(text: str) -> str:
    cleaned = ' '.join(str(text).strip().split())
    if not cleaned:
        return ''
    cleaned = cleaned[0].lower() + cleaned[1:] if len(cleaned) > 1 else cleaned.lower()
    if cleaned[-1] not in '.!?':
        cleaned += '.'
    return cleaned


def _build_email_body(
    report_day: date,
    metric_cards: list[MetricCard],
    submitted_items: list[RecapItem],
    top_risks: list[tuple[Person, ReportAnswerRecord]],
    assigned_follow_ups: list[tuple[Person, ReportAnswerRecord]],
    missing: list[Person],
) -> str:
    lines = [
        f'Subject: End-of-day recap for {report_day.isoformat()}',
        '',
        'Team,',
        '',
        'Yesterday snapshot:',
    ]
    lines.extend(f'- {metric.label}: {metric.value}' for metric in metric_cards)
    lines.extend(['', 'People updates:'])
    if submitted_items:
        lines.extend(f'- {item.summary_line}' for item in submitted_items)
    else:
        lines.append('- No submitted updates yet.')
    lines.extend(['', 'Risks to watch:'])
    if top_risks:
        lines.extend(f'- {person.name}: {_normalize_sentence(answer.answer_value)}' for person, answer in top_risks)
    else:
        lines.append('- No explicit risks submitted.')
    lines.extend(['', 'Follow-ups needing action:'])
    if assigned_follow_ups:
        lines.extend(
            f'- {person.name}: {answer.question_text} — {_normalize_sentence(answer.answer_value)}'
            for person, answer in assigned_follow_ups
        )
    else:
        lines.append('- No manager-assigned follow-ups submitted.')
    lines.extend(['', 'Missing inputs:'])
    if missing:
        lines.extend(f'- {person.name} — {person.role}' for person in missing)
    else:
        lines.append('- None.')
    return '\n'.join(lines)
