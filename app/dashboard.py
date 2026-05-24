from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.models import LEADERSHIP_SECTIONS, LeadershipSection, Person, ReportAnswerRecord, ReportRecord


@dataclass(frozen=True)
class KpiMetric:
    label: str
    value: str
    tone: str = 'neutral'


@dataclass(frozen=True)
class PriorityColumn:
    title: str
    items: list[str]


@dataclass(frozen=True)
class StatusCard:
    title: str
    detail: str
    tone: str


@dataclass(frozen=True)
class IntegrationCard:
    title: str
    summary: str
    detail: str


@dataclass(frozen=True)
class DashboardSectionView:
    section: LeadershipSection
    owner: Person
    health: str
    reported_priorities: list[str]
    ai_priorities: list[str]
    status_cards: list[StatusCard]
    summary: str


@dataclass(frozen=True)
class RollupView:
    label: str
    owner: Person
    health: str
    bullets: list[str]


@dataclass(frozen=True)
class DashboardView:
    report_day: date
    kpis: list[KpiMetric]
    ai_brief: list[str]
    milwaukee_rollup: RollupView
    milwaukee_sections: list[DashboardSectionView]
    slc_section: DashboardSectionView
    integrations: list[IntegrationCard]
    cpo_card: IntegrationCard


@dataclass(frozen=True)
class ExecutiveRecapView:
    report_day: date
    top_summary: list[str]
    milwaukee_summary: RollupView
    milwaukee_sections: list[DashboardSectionView]
    slc_summary: DashboardSectionView
    missing_people: list[Person]
    employee_ai_recap: list[str]
    integration_cards: list[IntegrationCard]
    cpo_card: IntegrationCard


def build_dashboard(report_day: date, people: list[Person], reports: list[ReportRecord]) -> DashboardView:
    people_by_id = {person.id: person for person in people}
    reports_by_person = {report.person_id: report for report in reports}
    missing_people = [person for person in people if person.id not in reports_by_person]

    all_sections = [
        _build_section(section, people_by_id, reports_by_person)
        for section in LEADERSHIP_SECTIONS
    ]
    milwaukee_rollup = _build_rollup(
        label='Milwaukee roll-up',
        owner=people_by_id['ricardo'],
        sections=[section for section in all_sections if section.section.location == 'Milwaukee' and section.section.kind == 'function'],
        missing_people=missing_people,
    )
    ai_brief = _build_ai_brief(all_sections, missing_people, reports)
    kpis = [
        KpiMetric('Reports in', str(len(reports))),
        KpiMetric('Missing', str(len(missing_people)), tone='warning' if missing_people else 'good'),
        KpiMetric('Risks', str(sum(1 for report in reports if _risk_answer(report))), tone='warning'),
        KpiMetric('Escalations', str(sum(len(_assigned_answers(report)) for report in reports)), tone='accent'),
    ]

    integrations = [
        IntegrationCard('ClickUp', 'AI recap pending live integration', 'Top fake data: 4 tasks at risk, 2 blockers surfaced.'),
        IntegrationCard('Slack', 'AI recap pending live integration', 'Top fake data: staffing concern mentioned twice, one dock escalation.'),
        IntegrationCard('Email', 'AI recap pending live integration', 'Top fake data: 3 customer-impact threads need review.'),
    ]
    cpo_card = IntegrationCard(
        'CPO / labor / out-of-SLA',
        'Placeholder operating block until App Script feed is wired.',
        'Fake data: Milwaukee labor -1 after 3 PM; 6 out-of-SLA orders need leadership eyes.',
    )

    return DashboardView(
        report_day=report_day,
        kpis=kpis,
        ai_brief=ai_brief,
        milwaukee_rollup=milwaukee_rollup,
        milwaukee_sections=[section for section in all_sections if section.section.location == 'Milwaukee' and section.section.kind == 'function'],
        slc_section=next(section for section in all_sections if section.section.id == 'salt-lake-city-operations'),
        integrations=integrations,
        cpo_card=cpo_card,
    )


def build_executive_recap(report_day: date, people: list[Person], reports: list[ReportRecord]) -> ExecutiveRecapView:
    dashboard = build_dashboard(report_day=report_day, people=people, reports=reports)
    reports_by_person = {report.person_id: report for report in reports}
    missing_people = [person for person in people if person.id not in reports_by_person]

    employee_ai_recap = [
        f"{section.owner.name}: {section.summary}"
        for section in dashboard.milwaukee_sections + [dashboard.slc_section]
    ]
    if not employee_ai_recap:
        employee_ai_recap = ['No employee reports submitted yet.']

    top_summary = [
        dashboard.ai_brief[0] if dashboard.ai_brief else 'No submitted reports yet.',
        f"Milwaukee health is {dashboard.milwaukee_rollup.health.lower()} with {len(dashboard.milwaukee_sections)} tracked sections.",
        f"Missing inputs: {', '.join(person.name for person in missing_people[:4]) or 'none'}.",
    ]

    return ExecutiveRecapView(
        report_day=report_day,
        top_summary=top_summary,
        milwaukee_summary=dashboard.milwaukee_rollup,
        milwaukee_sections=dashboard.milwaukee_sections,
        slc_summary=dashboard.slc_section,
        missing_people=missing_people,
        employee_ai_recap=employee_ai_recap,
        integration_cards=dashboard.integrations,
        cpo_card=dashboard.cpo_card,
    )


def _build_section(
    section: LeadershipSection,
    people_by_id: dict[str, Person],
    reports_by_person: dict[str, ReportRecord],
) -> DashboardSectionView:
    owner = people_by_id[section.owner_person_id]
    report = reports_by_person.get(owner.id)
    reported_priorities = _extract_top_three_priorities(report)
    ai_priorities = _build_ai_priorities(owner, report, reported_priorities)
    health = _health_from_report(report)
    status_cards = _build_status_cards(owner, report)
    summary = report.summary_text if report and report.summary_text.strip() else f'No report submitted yet for {owner.name}.'
    return DashboardSectionView(
        section=section,
        owner=owner,
        health=health,
        reported_priorities=reported_priorities,
        ai_priorities=ai_priorities,
        status_cards=status_cards,
        summary=summary,
    )


def _build_rollup(label: str, owner: Person, sections: list[DashboardSectionView], missing_people: list[Person]) -> RollupView:
    risk_sections = [section for section in sections if section.health in {'Yellow', 'Red'}]
    owner_summary = next((section.summary for section in sections if section.owner.id == owner.id and section.summary), '')
    owner_risks = [card.detail for section in sections if section.owner.id == owner.id for card in section.status_cards if card.title == 'Watch']
    bullets = [
        f"Overall Milwaukee health: {'steady' if not risk_sections else 'needs attention'}.",
        f"Open priorities across Milwaukee sections: {sum(len(section.reported_priorities) for section in sections)} captured.",
        f"Missing Milwaukee inputs: {', '.join(person.name for person in missing_people if person.manager_id in {'ricardo', 'cody', 'luis', 'adam', 'emily', 'hugh'}) or 'none'}.",
    ]
    if owner_summary:
        bullets.append(owner_summary)
    if owner_risks:
        bullets.append(owner_risks[0])
    if risk_sections:
        bullets.append(f"Biggest section at risk: {risk_sections[0].section.label}.")
    return RollupView(label=label, owner=owner, health='Yellow' if risk_sections else 'Green', bullets=bullets)


def _build_ai_brief(
    sections: list[DashboardSectionView],
    missing_people: list[Person],
    reports: list[ReportRecord],
) -> list[str]:
    submitted_sections = [section for section in sections if section.summary and not section.summary.startswith('No report submitted yet')]
    first_summary = submitted_sections[0].summary if submitted_sections else (reports[0].summary_text if reports else 'No submitted reports yet.')
    first_watch = next(
        (answer.answer_value for report in reports for answer in report.answers if answer.question_key.endswith('-risk') and answer.answer_value.strip()),
        next(
            (
                card.detail
                for section in sections
                for card in section.status_cards
                if card.title == 'Watch'
            ),
            'No immediate watch item surfaced.',
        ),
    )
    return [
        f"Fast take: {first_summary}",
        first_watch,
        f"Missing input count is {len(missing_people)}.",
        f"Priority sections needing leadership eyes: {', '.join(section.section.label for section in sections[:3])}.",
    ]


def _extract_top_three_priorities(report: ReportRecord | None) -> list[str]:
    if report is None:
        return ['No priorities submitted yet.']
    for answer in report.answers:
        if answer.question_key.endswith('-top3') and answer.answer_value.strip():
            raw_lines = [line.strip(' -•\t') for line in answer.answer_value.splitlines() if line.strip()]
            cleaned = [line for line in raw_lines if line]
            return cleaned[:3] or ['No priorities submitted yet.']
    return ['No priorities submitted yet.']


def _build_ai_priorities(owner: Person, report: ReportRecord | None, reported_priorities: list[str]) -> list[str]:
    risk = _risk_answer(report)
    summary = report.summary_text.strip() if report and report.summary_text.strip() else f'Need fresh read from {owner.name}.'
    ai = [
        f"Protect the biggest risk area for {owner.name.lower()}.",
        summary,
    ]
    if risk:
        ai.append(risk.answer_value)
    else:
        ai.append(reported_priorities[0] if reported_priorities else 'No AI priority available yet.')
    return ai[:3]


def _build_status_cards(owner: Person, report: ReportRecord | None) -> list[StatusCard]:
    if report is None:
        return [StatusCard('Missing input', f'{owner.name} did not submit an update.', 'warning')]
    risk = _risk_answer(report)
    cards = [StatusCard('Submitted', owner.role, 'good')]
    if risk and risk.answer_value.strip():
        cards.append(StatusCard('Watch', risk.answer_value, 'warning'))
    assigned = _assigned_answers(report)
    if assigned:
        cards.append(StatusCard('Escalations', assigned[0].answer_value, 'accent'))
    return cards


def _risk_answer(report: ReportRecord | None) -> ReportAnswerRecord | None:
    if report is None:
        return None
    return next((answer for answer in report.answers if answer.question_key.endswith('-risk') and answer.answer_value.strip()), None)


def _assigned_answers(report: ReportRecord | None) -> list[ReportAnswerRecord]:
    if report is None:
        return []
    return [answer for answer in report.answers if answer.source == 'manager-assigned' and answer.answer_value.strip()]


def _health_from_report(report: ReportRecord | None) -> str:
    if report is None:
        return 'Red'
    risk = _risk_answer(report)
    if risk:
        return 'Yellow'
    return 'Green'
