from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_route_returns_ok():
    response = client.get('/health')

    assert response.status_code == 200
    assert response.json() == {'ok': True}


def test_manifest_route_returns_installable_metadata():
    response = client.get('/manifest.webmanifest')

    assert response.status_code == 200
    assert response.headers['content-type'].startswith('application/manifest+json')
    body = response.json()
    assert body['name'] == 'Operations Report'
    assert body['display'] == 'standalone'
    assert body['start_url'] == '/'
    assert any(icon['src'] == '/assets/app-icon-192.png' for icon in body['icons'])


def test_service_worker_route_registers_shell_assets():
    response = client.get('/sw.js')

    assert response.status_code == 200
    assert 'self.addEventListener' in response.text
    assert '/manifest.webmanifest' in response.text
    assert '/assets/pwa.js' in response.text


def test_root_route_returns_operations_report_intake_markers():
    response = client.get('/')

    assert response.status_code == 200
    assert 'Operations Report' in response.text
    assert 'Choose your name' in response.text
    assert 'Start report' in response.text
    assert 'Leadership tools' in response.text
    assert '/manager?person_id=drake' in response.text
    assert '/manager?person_id=ricardo' in response.text
    assert '/manager?person_id=norman' in response.text
    assert '/manager?person_id=hugh' in response.text
    assert '/manager?person_id=emily' in response.text
    assert '/dashboard' in response.text
    assert '/recap' in response.text
    assert '/design-preview' in response.text
    assert 'href="/manifest.webmanifest"' in response.text
    assert 'id="installAppButton"' in response.text
    assert 'Industrial command shell' in response.text
    assert 'data-ui="intake-actions"' in response.text


def test_design_preview_route_renders_aggressive_pass_markers():
    response = client.get('/design-preview')

    assert response.status_code == 200
    assert 'Aggressive redesign + cleanup preview' in response.text
    assert 'Daily operating picture with the dead weight stripped out.' in response.text
    assert 'Milwaukee control band' in response.text
    assert 'Canonical structure' in response.text
    assert 'FastAPI is canonical' in response.text


def test_dashboard_route_renders_graph_markers():
    response = client.get('/dashboard')

    assert response.status_code == 200
    assert 'Ops' in response.text
    assert 'Ops summary' in response.text
    assert 'Key metrics' in response.text
    assert 'Ops notes' in response.text
    assert 'Report coverage' in response.text
    assert 'Open issues by team' in response.text
    assert 'Milwaukee' in response.text
    assert 'Generate recap' in response.text
    assert 'data-ui="dashboard-nav"' in response.text
    assert 'data-ui="control-band"' in response.text
    assert 'svg' in response.text
    assert 'Ricardo' in response.text
    assert 'Hugh' in response.text


def test_root_route_renders_real_org_roster_markers():
    response = client.get('/')

    assert response.status_code == 200
    assert 'Drake — VP Operations • Leadership' in response.text
    assert 'Ricardo — Milwaukee operations manager • Milwaukee' in response.text
    assert 'Norman — Salt Lake City operations manager • Salt Lake City' in response.text
    assert 'Kody — Milwaukee outbound manager • Milwaukee' in response.text
    assert 'Ramar — Unload lead • Night shift' in response.text
    assert 'Yaniel — Shipping coordinator • Night shift' in response.text
    assert 'Anna — Packing lead • Night shift' in response.text
    assert 'Rely — Returns coordinator • Closing shift' in response.text
    assert 'Santana — Project coordinator • Day shift' in response.text
    assert 'Founder mode' not in response.text
    assert 'value="rely"' in response.text
    assert 'value="santana"' in response.text
    assert 'Cody — Outbound supervisor • 2nd shift' not in response.text
    assert 'Ana — Packing lead • Night shift' not in response.text
    assert 'Ophelia — Dock coordinator • Night shift' not in response.text
    assert 'Maria L — Replenishment lead • Swing shift' not in response.text


def test_report_form_route_renders_selected_person_questions():
    response = client.get('/reports/new?person_id=cody')

    assert response.status_code == 200
    assert 'Kody' in response.text
    assert 'Milwaukee outbound manager' in response.text
    assert 'How are we doing, Kody?' in response.text
    assert 'What are your top 3 priorities for tomorrow?' in response.text
    assert 'What is the one thing leadership should watch tomorrow?' in response.text
    assert 'Submit report' in response.text
    assert 'Cody' not in response.text


def test_submit_report_route_redirects_to_confirmation_page():
    response = client.post(
        '/reports',
        data={
            'person_id': 'cody',
            'cody-mood': 'Good',
            'cody-wins': 'Backlog cleared before carrier cutoff.',
            'cody-risk': 'Need one more picker after 3 PM tomorrow.',
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers['location'].startswith('/reports/')

    confirmation = client.get(response.headers['location'])

    assert confirmation.status_code == 200
    assert 'Report submitted' in confirmation.text
    assert 'Kody' in confirmation.text
    assert 'Backlog cleared before carrier cutoff.' in confirmation.text



def test_manager_page_renders_hierarchy_scoped_assignee_list():
    response = client.get('/manager?person_id=ricardo')

    assert response.status_code == 200
    assert 'Assign questions' in response.text
    assert 'Ricardo' in response.text
    assert 'value="drake"' in response.text
    assert 'value="norman"' in response.text
    assert 'value="cody"' in response.text
    assert 'value="ana"' in response.text
    assert 'value="rely"' in response.text
    assert 'value="santana"' in response.text


def test_midlevel_manager_page_only_shows_direct_team_scope():
    response = client.get('/manager?person_id=cody')

    assert response.status_code == 200
    assert 'Assign questions' in response.text
    assert 'Kody' in response.text
    assert 'value="ana"' in response.text
    assert 'value="danielle"' in response.text
    assert 'value="brenda"' not in response.text
    assert 'value="rely"' not in response.text
    assert 'value="santana"' not in response.text



def test_manager_page_supports_new_single_report_emily_scope():
    response = client.get('/manager?person_id=emily')

    assert response.status_code == 200
    assert 'Emily' in response.text
    assert 'value="rely"' in response.text
    assert 'value="ana"' not in response.text


def test_manager_page_rejects_non_manager_picker():
    response = client.get('/manager?person_id=rely')

    assert response.status_code == 403



def test_create_assignment_route_redirects_and_assignment_appears_in_target_report():
    response = client.post(
        '/manager/assignments',
        data={
            'created_by_person_id': 'ricardo',
            'assigned_to_person_id': 'cody',
            'prompt': 'What shipment risk needs help before 10 AM?',
            'answer_type': 'text',
            'helper_text': 'One escalation only.',
            'cadence': 'daily',
        },
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers['location'].startswith('/manager?person_id=ricardo&assignment_id=')

    manager_page = client.get(response.headers['location'])
    assert manager_page.status_code == 200
    assert 'Kody — Milwaukee outbound manager' in manager_page.text
    assert 'What shipment risk needs help before 10 AM?' in manager_page.text
    assert 'Pause question' in manager_page.text
    assert 'Edit question' in manager_page.text

    report_form = client.get('/reports/new?person_id=cody')

    assert report_form.status_code == 200
    assert 'What shipment risk needs help before 10 AM?' in report_form.text
    assert 'One escalation only.' in report_form.text


def test_update_assignment_route_edits_existing_question_and_redirects_back_to_manager():
    create_response = client.post(
        '/manager/assignments',
        data={
            'created_by_person_id': 'ricardo',
            'assigned_to_person_id': 'cody',
            'prompt': 'Old prompt',
            'answer_type': 'text',
            'helper_text': 'Old helper',
            'cadence': 'daily',
        },
        follow_redirects=False,
    )
    assignment_id = create_response.headers['location'].split('assignment_id=')[1]

    update_response = client.post(
        f'/manager/assignments/{assignment_id}/edit',
        data={
            'created_by_person_id': 'ricardo',
            'assigned_to_person_id': 'cody',
            'prompt': 'Updated shipment risk before 10 AM?',
            'answer_type': 'textarea',
            'helper_text': 'Give one crisp blocker.',
            'cadence': 'daily',
        },
        follow_redirects=False,
    )

    assert update_response.status_code == 303
    assert update_response.headers['location'] == f'/manager?person_id=ricardo&assignment_id={assignment_id}'

    manager_page = client.get(update_response.headers['location'])
    assert manager_page.status_code == 200
    assert 'Updated shipment risk before 10 AM?' in manager_page.text
    assert 'Give one crisp blocker.' in manager_page.text
    assert 'daily' in manager_page.text

    report_form = client.get('/reports/new?person_id=cody')
    assert report_form.status_code == 200
    assert 'Updated shipment risk before 10 AM?' in report_form.text


def test_pause_assignment_route_hides_question_from_target_report_until_resumed():
    create_response = client.post(
        '/manager/assignments',
        data={
            'created_by_person_id': 'ricardo',
            'assigned_to_person_id': 'cody',
            'prompt': 'What needs help tonight?',
            'answer_type': 'text',
            'helper_text': 'Keep it short.',
            'cadence': 'daily',
        },
        follow_redirects=False,
    )
    assignment_id = create_response.headers['location'].split('assignment_id=')[1]
    unique_prompt = f'What needs help tonight #{assignment_id}?'

    client.post(
        f'/manager/assignments/{assignment_id}/edit',
        data={
            'created_by_person_id': 'ricardo',
            'assigned_to_person_id': 'cody',
            'prompt': unique_prompt,
            'answer_type': 'text',
            'helper_text': 'Keep it short.',
            'cadence': 'daily',
        },
        follow_redirects=False,
    )

    pause_response = client.post(
        f'/manager/assignments/{assignment_id}/pause',
        data={'created_by_person_id': 'ricardo'},
        follow_redirects=False,
    )
    assert pause_response.status_code == 303
    assert pause_response.headers['location'] == f'/manager?person_id=ricardo&assignment_id={assignment_id}'

    report_form = client.get('/reports/new?person_id=cody')
    assert report_form.status_code == 200
    assert unique_prompt not in report_form.text

    manager_page = client.get(pause_response.headers['location'])
    assert 'Resume question' in manager_page.text
    assert 'Inactive' in manager_page.text

    resume_response = client.post(
        f'/manager/assignments/{assignment_id}/resume',
        data={'created_by_person_id': 'ricardo'},
        follow_redirects=False,
    )
    assert resume_response.status_code == 303

    resumed_report_form = client.get('/reports/new?person_id=cody')
    assert resumed_report_form.status_code == 200
    assert unique_prompt in resumed_report_form.text



def test_dashboard_page_shows_saved_reports_for_today():
    client.post(
        '/reports',
        data={
            'person_id': 'ricardo',
            'ricardo-mood': 'Good',
            'ricardo-wins': 'Recovered dock backlog before cutoff.',
            'ricardo-top3': '1. Cover Milwaukee outbound labor\n2. Clear inventory blockers\n3. Review second shift handoff',
            'ricardo-risk': 'Need more outbound coverage after 3 PM.',
        },
        follow_redirects=False,
    )

    response = client.get('/dashboard')

    assert response.status_code == 200
    assert 'Leadership dashboard' in response.text
    assert 'Ops notes' in response.text
    assert 'Generate recap' in response.text
    assert 'Open recap' in response.text
    assert 'Start report' in response.text
    assert 'Manage questions' in response.text
    assert 'Milwaukee' in response.text
    assert 'Milwaukee Outbound' in response.text
    assert 'Milwaukee Inventory' in response.text
    assert 'Milwaukee Inbound / Returns' in response.text
    assert 'Milwaukee 2nd Shift' in response.text
    assert 'Milwaukee Special Projects / B2B' in response.text
    assert 'Salt Lake City Operations' in response.text
    assert 'ClickUp' in response.text
    assert 'Slack' in response.text
    assert 'Email' in response.text
    assert 'CPO / labor / out-of-SLA' in response.text
    assert 'Recovered dock backlog before cutoff.' in response.text
    assert 'Missing input count is' in response.text



def test_execute_recap_review_page_renders_executive_sections():
    client.post(
        '/reports',
        data={
            'person_id': 'ricardo',
            'ricardo-mood': 'Good',
            'ricardo-wins': 'Recovered dock backlog before cutoff.',
            'ricardo-top3': '1. Cover Milwaukee outbound labor\n2. Clear inventory blockers\n3. Review second shift handoff',
            'ricardo-risk': 'Need more outbound coverage after 3 PM.',
        },
        follow_redirects=False,
    )

    response = client.get('/execute-recap')

    assert response.status_code == 200
    assert 'Executive recap review' in response.text
    assert 'Milwaukee summary' in response.text
    assert 'Salt Lake City summary' in response.text
    assert 'Employee report AI recap' in response.text
    assert 'ClickUp AI recap' in response.text
    assert 'Slack AI recap' in response.text
    assert 'Gmail AI recap' in response.text
    assert 'CPO / labor / out-of-SLA' in response.text



def test_recap_page_groups_submissions_missing_people_and_assigned_answers():
    assignment_response = client.post(
        '/manager/assignments',
        data={
            'created_by_person_id': 'ricardo',
            'assigned_to_person_id': 'cody',
            'prompt': 'What exactly needs leadership help tomorrow morning?',
            'answer_type': 'text',
            'helper_text': 'One concrete escalation.',
            'cadence': 'daily',
        },
        follow_redirects=False,
    )
    assignment_id = assignment_response.headers['location'].split('assignment_id=')[1]

    client.post(
        '/reports',
        data={
            'person_id': 'ricardo',
            'ricardo-mood': 'Good',
            'ricardo-wins': 'Recovered dock backlog before cutoff.',
            'ricardo-risk': 'Need more outbound coverage after 3 PM.',
            'ricardo-yesterday-labor-hours-spent': '18',
            'ricardo-yesterday-hours-worked': '42',
            'ricardo-yesterday-orders-shipped': '380',
            'ricardo-yesterday-units-per-hour': '27.4',
            'ricardo-yesterday-cost-per-order': '2.85',
            'ricardo-yesterday-orders-missed-sla': '7',
        },
        follow_redirects=False,
    )
    client.post(
        '/reports',
        data={
            'person_id': 'hugh',
            'hugh-mood': 'Good',
            'hugh-wins': 'Stabilized second shift staffing and cleared the carryover queue.',
            'hugh-risk': 'Two newer packers still need closer coaching on late wave accuracy.',
            'hugh-yesterday-labor-hours-spent': '9',
            'hugh-yesterday-hours-worked': '18',
            'hugh-yesterday-orders-shipped': '110',
            'hugh-yesterday-units-per-hour': '22',
            'hugh-yesterday-cost-per-order': '3.40',
            'hugh-yesterday-orders-missed-sla': '4',
        },
        follow_redirects=False,
    )
    client.post(
        '/reports',
        data={
            'person_id': 'cody',
            'cody-mood': 'Okay',
            'cody-wins': 'Trailer pull timing improved before close.',
            'cody-risk': 'Need one more picker after 3 PM tomorrow.',
            f'assignment-{assignment_id}': 'Need temp labor approved before first outbound wave.',
        },
        follow_redirects=False,
    )

    response = client.get('/recap')

    assert response.status_code == 200
    assert 'Recap' in response.text
    assert 'Yesterday' in response.text
    assert 'Manager updates' in response.text
    assert 'Yesterday&#39;s labor hours spent' in response.text
    assert 'Yesterday&#39;s hours worked' in response.text
    assert 'Yesterday&#39;s orders shipped' in response.text
    assert 'Yesterday&#39;s units per hour' in response.text
    assert 'Yesterday&#39;s cost per order' in response.text
    assert 'Yesterday&#39;s orders that missed SLA' in response.text
    assert 'Email draft' in response.text
    assert 'data-ui="email-draft"' in response.text
    assert 'Subject: End-of-day recap for' in response.text
    assert 'Ricardo reported recovered dock backlog before cutoff.' in response.text
    assert 'Hugh reported stabilized second shift staffing and cleared the carryover queue.' in response.text
    assert 'Kody reported trailer pull timing improved before close.' in response.text
    assert 'Two newer packers still need closer coaching on late wave accuracy.' in response.text
    assert 'Rely' in response.text
    assert 'What exactly needs leadership help tomorrow morning?' in response.text
    assert 'Need temp labor approved before first outbound wave.' in response.text
