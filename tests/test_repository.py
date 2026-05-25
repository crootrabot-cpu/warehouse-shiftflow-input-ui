from datetime import date

from app.models import QuestionAssignmentInput, ReportAnswerInput, ReportInput
from app.repository import SQLiteRepository


PERSON_IDS = {
    'drake', 'ricardo', 'norman', 'cody', 'hugh', 'luis', 'adam', 'emily',
    'ana', 'danielle', 'brenda', 'remar', 'edwin', 'maria', 'nate',
    'rely', 'santana',
}


def build_repo(tmp_path):
    db_path = tmp_path / 'operations-report.db'
    repo = SQLiteRepository(db_path)
    repo.init_schema()
    return repo


def test_repository_seeds_expected_people_roster(tmp_path):
    repo = build_repo(tmp_path)

    people = repo.list_people()
    people_by_id = {person.id: person for person in people}

    assert {person.id for person in people} == PERSON_IDS
    assert people_by_id['ricardo'].manager_id == 'drake'
    assert people_by_id['norman'].manager_id == 'drake'
    assert people_by_id['cody'].manager_id == 'ricardo'
    assert people_by_id['hugh'].manager_id == 'ricardo'
    assert people_by_id['nate'].manager_id == 'adam'
    assert people_by_id['rely'].manager_id == 'emily'
    assert people_by_id['santana'].manager_id == 'norman'
    assert people_by_id['drake'].can_assign is True
    assert people_by_id['norman'].can_assign is True
    assert people_by_id['emily'].can_assign is True
    assert people_by_id['hugh'].can_assign is True
    assert people_by_id['ana'].can_assign is False
    assert people_by_id['drake'].role == 'VP Operations'
    assert people_by_id['cody'].name == 'Kody'
    assert people_by_id['cody'].role == 'Milwaukee outbound manager'
    assert people_by_id['ricardo'].role == 'Milwaukee operations manager'
    assert people_by_id['norman'].role == 'Salt Lake City operations manager'
    assert people_by_id['hugh'].role == 'Milwaukee second shift manager'
    assert people_by_id['luis'].role == 'Milwaukee inventory manager'
    assert people_by_id['adam'].role == 'Milwaukee special projects / B2B manager'
    assert people_by_id['emily'].role == 'Milwaukee inbound / returns manager'
    assert people_by_id['ana'].name == 'Anna'
    assert people_by_id['remar'].name == 'Ramar'
    assert people_by_id['danielle'].name == 'Yaniel'
    assert people_by_id['rely'].name == 'Rely'
    assert people_by_id['santana'].name == 'Santana'



def test_save_report_persists_answers_and_is_returned_for_report_day(tmp_path):
    repo = build_repo(tmp_path)

    created = repo.save_report(
        ReportInput(
            person_id='ricardo',
            report_date=date(2026, 5, 24),
            summary_text='Strong dock recovery before cutoff.',
            answers=[
                ReportAnswerInput(
                    question_key='ricardo-mood',
                    question_text='How are we doing, Ricardo?',
                    answer_value='Good',
                    answer_type='choice',
                    source='default',
                ),
                ReportAnswerInput(
                    question_key='ricardo-top3',
                    question_text='What are your top 3 priorities for tomorrow?',
                    answer_value='1. Cover Milwaukee outbound labor\n2. Clear inventory blockers\n3. Review second shift handoff',
                    answer_type='textarea',
                    source='default',
                ),
                ReportAnswerInput(
                    question_key='ricardo-risk',
                    question_text='What is the one thing leadership should watch tomorrow?',
                    answer_value='Late labor gap in outbound after 3 PM.',
                    answer_type='text',
                    source='default',
                ),
            ],
        )
    )

    reports = repo.list_reports_for_day(date(2026, 5, 24))

    assert created.id is not None
    assert len(reports) == 1
    assert reports[0].person_id == 'ricardo'
    assert reports[0].summary_text == 'Strong dock recovery before cutoff.'
    assert [answer.question_key for answer in reports[0].answers] == ['ricardo-mood', 'ricardo-top3', 'ricardo-risk']
    assert reports[0].answers[1].answer_value.startswith('1. Cover Milwaukee outbound labor')
    assert reports[0].answers[2].answer_value == 'Late labor gap in outbound after 3 PM.'



def test_save_assignment_persists_and_scopes_to_assignee(tmp_path):
    repo = build_repo(tmp_path)

    created = repo.save_assignment(
        QuestionAssignmentInput(
            created_by_person_id='ricardo',
            assigned_to_person_id='cody',
            prompt='What is the biggest pickup risk in outbound before first truck close?',
            answer_type='textarea',
            helper_text='One clean operational note.',
            cadence='daily',
            active=True,
        )
    )

    cody_assignments = repo.list_assignments_for_person('cody')
    luis_assignments = repo.list_assignments_for_person('luis')

    assert created.id is not None
    assert len(cody_assignments) == 1
    assert cody_assignments[0].prompt.startswith('What is the biggest pickup risk')
    assert cody_assignments[0].created_by_person_id == 'ricardo'
    assert luis_assignments == []



def test_questions_for_person_merge_default_and_active_manager_assigned_questions(tmp_path):
    repo = build_repo(tmp_path)
    repo.save_assignment(
        QuestionAssignmentInput(
            created_by_person_id='ricardo',
            assigned_to_person_id='cody',
            prompt='What needs executive help before 10 AM tomorrow?',
            answer_type='text',
            helper_text='Escalate only what really matters.',
            cadence='daily',
            active=True,
        )
    )

    questions = repo.get_questions_for_person('cody', on_date=date(2026, 5, 24))

    assert [question.source for question in questions[:3]] == ['default', 'default', 'default']
    assert questions[-1].source == 'manager-assigned'
    assert questions[-1].prompt == 'What needs executive help before 10 AM tomorrow?'
    assert questions[-1].helper == 'Escalate only what really matters.'



def test_get_assignable_people_matches_revised_manager_rules(tmp_path):
    repo = build_repo(tmp_path)

    ricardo_targets = [person.id for person in repo.get_assignable_people('ricardo')]
    drake_targets = [person.id for person in repo.get_assignable_people('drake')]
    norman_targets = [person.id for person in repo.get_assignable_people('norman')]
    cody_targets = [person.id for person in repo.get_assignable_people('cody')]
    adam_targets = [person.id for person in repo.get_assignable_people('adam')]
    luis_targets = [person.id for person in repo.get_assignable_people('luis')]
    emily_targets = [person.id for person in repo.get_assignable_people('emily')]
    rely_targets = repo.get_assignable_people('rely')

    assert ricardo_targets == [
        'drake', 'ricardo', 'norman', 'cody', 'hugh', 'luis', 'adam', 'emily',
        'danielle', 'ana', 'remar', 'brenda', 'nate', 'maria', 'edwin',
        'rely', 'santana',
    ]
    assert drake_targets == ricardo_targets
    assert norman_targets == ricardo_targets
    assert cody_targets == ['danielle', 'ana']
    assert adam_targets == ['nate', 'maria', 'edwin']
    assert luis_targets == ['remar', 'brenda']
    assert emily_targets == ['rely']
    assert rely_targets == []



def test_update_assignment_persists_new_fields_and_active_toggle_controls_visibility(tmp_path):
    repo = build_repo(tmp_path)
    created = repo.save_assignment(
        QuestionAssignmentInput(
            created_by_person_id='ricardo',
            assigned_to_person_id='cody',
            prompt='Old prompt',
            answer_type='text',
            helper_text='Old helper',
            cadence='daily',
            active=True,
        )
    )

    updated = repo.update_assignment(
        assignment_id=created.id,
        created_by_person_id='ricardo',
        assigned_to_person_id='cody',
        prompt='Updated prompt',
        answer_type='textarea',
        helper_text='Updated helper',
        cadence='weekdays',
    )

    assert updated.prompt == 'Updated prompt'
    assert updated.answer_type == 'textarea'
    assert updated.helper_text == 'Updated helper'
    assert updated.cadence == 'weekdays'
    assert updated.days == ['mon', 'tue', 'wed', 'thu', 'fri']

    active_questions = repo.get_questions_for_person('cody', on_date=date(2026, 5, 25))
    assert active_questions[-1].prompt == 'Updated prompt'

    paused = repo.set_assignment_active(created.id, active=False)
    assert paused.active is False
    paused_questions = repo.get_questions_for_person('cody', on_date=date(2026, 5, 25))
    assert all(question.prompt != 'Updated prompt' for question in paused_questions)

    resumed = repo.set_assignment_active(created.id, active=True)
    assert resumed.active is True
    resumed_questions = repo.get_questions_for_person('cody', on_date=date(2026, 5, 25))
    assert resumed_questions[-1].prompt == 'Updated prompt'
