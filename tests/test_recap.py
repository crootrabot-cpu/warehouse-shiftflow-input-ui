from datetime import date, datetime

from app.models import PEOPLE, ReportAnswerRecord, ReportRecord
from app.recap import build_recap


def _report(person_id: str, summary: str, risk: str, metrics: dict[str, str]) -> ReportRecord:
    answers = [
        ReportAnswerRecord(
            question_key=f'{person_id}-risk',
            question_text='What is the one thing leadership should watch tomorrow?',
            answer_value=risk,
            answer_type='text',
            source='default',
        ),
    ]
    for key, value in metrics.items():
        answers.append(
            ReportAnswerRecord(
                question_key=f'{person_id}-{key}',
                question_text=key,
                answer_value=value,
                answer_type='number',
                source='default',
            )
        )
    return ReportRecord(
        id=1,
        person_id=person_id,
        report_date=date(2026, 5, 24),
        submitted_at=datetime(2026, 5, 24, 22, 0, 0),
        status='submitted',
        summary_text=summary,
        answers=answers,
    )


def test_build_recap_rolls_up_yesterday_metrics_and_email_summary():
    recap = build_recap(
        report_day=date(2026, 5, 24),
        people=PEOPLE,
        reports=[
            _report(
                'ricardo',
                'Recovered dock backlog before cutoff.',
                'Need more outbound coverage after 3 PM.',
                {
                    'yesterday-labor-hours-spent': '18',
                    'yesterday-hours-worked': '42',
                    'yesterday-orders-shipped': '380',
                    'yesterday-units-per-hour': '27.4',
                    'yesterday-cost-per-order': '2.85',
                    'yesterday-orders-missed-sla': '7',
                },
            ),
            _report(
                'hugh',
                'Stabilized second shift staffing and cleared the carryover queue.',
                'Two newer packers still need closer coaching on late wave accuracy.',
                {
                    'yesterday-labor-hours-spent': '9',
                    'yesterday-hours-worked': '18',
                    'yesterday-orders-shipped': '110',
                    'yesterday-units-per-hour': '22',
                    'yesterday-cost-per-order': '3.40',
                    'yesterday-orders-missed-sla': '4',
                },
            ),
            _report(
                'cody',
                'Trailer pull timing improved before close.',
                'Need one more picker after 3 PM tomorrow.',
                {},
            ),
        ],
    )

    assert [metric.value for metric in recap.metric_cards] == ['27.0', '60.0', '490', '25.8', '2.97', '11']
    assert recap.email_subject == 'End-of-day recap for 2026-05-24'
    assert 'Ricardo reported recovered dock backlog before cutoff.' in recap.email_body
    assert 'Hugh reported stabilized second shift staffing and cleared the carryover queue.' in recap.email_body
    assert 'Kody reported trailer pull timing improved before close.' in recap.email_body
    assert 'two newer packers still need closer coaching on late wave accuracy.' in recap.email_body
    assert 'Yesterday snapshot:' in recap.email_body
    assert "- Yesterday's cost per order: 2.97" in recap.email_body
