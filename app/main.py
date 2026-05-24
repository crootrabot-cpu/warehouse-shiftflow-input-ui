from datetime import date

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR, DATA_DIR, DATABASE_PATH
from app.dashboard import build_dashboard, build_executive_recap
from app.models import QuestionAssignmentInput, ReportAnswerInput, ReportInput
from app.recap import build_recap
from app.repository import SQLiteRepository

DATA_DIR.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))
repository = SQLiteRepository(DATABASE_PATH)
repository.init_schema()

app = FastAPI(title='Operations Report')


@app.get('/health')
def health() -> dict[str, bool]:
    return {'ok': True}


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    people = repository.list_people()
    managers = [person for person in people if person.can_assign]
    return templates.TemplateResponse(
        request=request,
        name='intake.html',
        context={'people': people, 'managers': managers},
    )


@app.get('/reports/new', response_class=HTMLResponse)
def new_report(request: Request, person_id: str):
    people = {person.id: person for person in repository.list_people()}
    person = people[person_id]
    questions = repository.get_questions_for_person(person_id, on_date=date.today())
    return templates.TemplateResponse(
        request=request,
        name='report_form.html',
        context={'person': person, 'questions': questions},
    )


@app.post('/reports')
async def create_report(request: Request, person_id: str = Form(...)):
    people = {person.id: person for person in repository.list_people()}
    person = people.get(person_id)
    if person is None:
        raise HTTPException(status_code=404, detail='Person not found')

    questions = repository.get_questions_for_person(person_id, on_date=date.today())
    form = await request.form()
    answers = []
    summary_text = ''
    for question in questions:
        answer_value = str(form.get(question.id, '')).strip()
        answers.append(
            ReportAnswerInput(
                question_key=question.id,
                question_text=question.prompt,
                answer_value=answer_value,
                answer_type=question.type,
                source=question.source,
            )
        )
        if question.id.endswith('-wins') and answer_value:
            summary_text = answer_value

    report = repository.save_report(
        ReportInput(
            person_id=person_id,
            report_date=date.today(),
            summary_text=summary_text,
            answers=answers,
        )
    )
    return RedirectResponse(url=f'/reports/{report.id}', status_code=303)


@app.get('/reports/{report_id}', response_class=HTMLResponse)
def report_detail(request: Request, report_id: int):
    report = repository.get_report(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail='Report not found')

    people = {person.id: person for person in repository.list_people()}
    person = people[report.person_id]
    return templates.TemplateResponse(
        request=request,
        name='report_submitted.html',
        context={'person': person, 'report': report},
    )


@app.get('/manager', response_class=HTMLResponse)
def manager_page(request: Request, person_id: str, assignment_id: int | None = None):
    manager = repository.get_person(person_id)
    if manager is None:
        raise HTTPException(status_code=404, detail='Person not found')
    if not manager.can_assign:
        raise HTTPException(status_code=403, detail='Person cannot assign questions')

    people = {person.id: person for person in repository.list_people()}
    assignable_people = repository.get_assignable_people(person_id)
    assignments = repository.list_assignments_created_by_person(person_id)
    selected_assignment = repository.get_assignment(assignment_id) if assignment_id is not None else None
    if selected_assignment is not None and selected_assignment.created_by_person_id != person_id:
        raise HTTPException(status_code=403, detail='Assignment not owned by manager')
    return templates.TemplateResponse(
        request=request,
        name='manager.html',
        context={
            'manager': manager,
            'assignable_people': assignable_people,
            'assignments': assignments,
            'people_by_id': people,
            'selected_assignment': selected_assignment,
        },
    )


@app.post('/manager/assignments')
def create_assignment(
    created_by_person_id: str = Form(...),
    assigned_to_person_id: str = Form(...),
    prompt: str = Form(...),
    answer_type: str = Form(...),
    helper_text: str = Form(''),
    cadence: str = Form('today'),
):
    manager = repository.get_person(created_by_person_id)
    if manager is None:
        raise HTTPException(status_code=404, detail='Manager not found')
    allowed_ids = {person.id for person in repository.get_assignable_people(created_by_person_id)}
    if assigned_to_person_id not in allowed_ids:
        raise HTTPException(status_code=403, detail='Assignment target not allowed')

    assignment = repository.save_assignment(
        QuestionAssignmentInput(
            created_by_person_id=created_by_person_id,
            assigned_to_person_id=assigned_to_person_id,
            prompt=prompt.strip(),
            answer_type=answer_type,
            helper_text=helper_text.strip(),
            cadence=cadence,
        )
    )
    return RedirectResponse(
        url=f'/manager?person_id={created_by_person_id}&assignment_id={assignment.id}',
        status_code=303,
    )


@app.post('/manager/assignments/{assignment_id}/edit')
def edit_assignment(
    assignment_id: int,
    created_by_person_id: str = Form(...),
    assigned_to_person_id: str = Form(...),
    prompt: str = Form(...),
    answer_type: str = Form(...),
    helper_text: str = Form(''),
    cadence: str = Form('today'),
):
    manager = repository.get_person(created_by_person_id)
    if manager is None or not manager.can_assign:
        raise HTTPException(status_code=403, detail='Manager not allowed')
    existing = repository.get_assignment(assignment_id)
    if existing is None:
        raise HTTPException(status_code=404, detail='Assignment not found')
    if existing.created_by_person_id != created_by_person_id:
        raise HTTPException(status_code=403, detail='Assignment not owned by manager')
    allowed_ids = {person.id for person in repository.get_assignable_people(created_by_person_id)}
    if assigned_to_person_id not in allowed_ids:
        raise HTTPException(status_code=403, detail='Assignment target not allowed')

    repository.update_assignment(
        assignment_id=assignment_id,
        created_by_person_id=created_by_person_id,
        assigned_to_person_id=assigned_to_person_id,
        prompt=prompt.strip(),
        answer_type=answer_type,
        helper_text=helper_text.strip(),
        cadence=cadence,
    )
    return RedirectResponse(
        url=f'/manager?person_id={created_by_person_id}&assignment_id={assignment_id}',
        status_code=303,
    )


@app.post('/manager/assignments/{assignment_id}/pause')
def pause_assignment(assignment_id: int, created_by_person_id: str = Form(...)):
    assignment = repository.get_assignment(assignment_id)
    if assignment is None:
        raise HTTPException(status_code=404, detail='Assignment not found')
    if assignment.created_by_person_id != created_by_person_id:
        raise HTTPException(status_code=403, detail='Assignment not owned by manager')
    repository.set_assignment_active(assignment_id, active=False)
    return RedirectResponse(
        url=f'/manager?person_id={created_by_person_id}&assignment_id={assignment_id}',
        status_code=303,
    )


@app.post('/manager/assignments/{assignment_id}/resume')
def resume_assignment(assignment_id: int, created_by_person_id: str = Form(...)):
    assignment = repository.get_assignment(assignment_id)
    if assignment is None:
        raise HTTPException(status_code=404, detail='Assignment not found')
    if assignment.created_by_person_id != created_by_person_id:
        raise HTTPException(status_code=403, detail='Assignment not owned by manager')
    repository.set_assignment_active(assignment_id, active=True)
    return RedirectResponse(
        url=f'/manager?person_id={created_by_person_id}&assignment_id={assignment_id}',
        status_code=303,
    )


@app.get('/dashboard', response_class=HTMLResponse)
def dashboard(request: Request):
    people = repository.list_people()
    reports = repository.list_reports_for_day(date.today())
    dashboard_view = build_dashboard(report_day=date.today(), people=people, reports=reports)

    return templates.TemplateResponse(
        request=request,
        name='dashboard.html',
        context={'dashboard': dashboard_view},
    )


@app.get('/design-preview', response_class=HTMLResponse)
def design_preview_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='design_preview.html',
        context={},
    )


@app.get('/execute-recap', response_class=HTMLResponse)
def execute_recap_page(request: Request):
    people = repository.list_people()
    reports = repository.list_reports_for_day(date.today())
    executive_recap = build_executive_recap(report_day=date.today(), people=people, reports=reports)
    return templates.TemplateResponse(
        request=request,
        name='execute_recap.html',
        context={'executive_recap': executive_recap},
    )


@app.get('/recap', response_class=HTMLResponse)
def recap_page(request: Request):
    people = repository.list_people()
    reports = repository.list_reports_for_day(date.today())
    recap = build_recap(report_day=date.today(), people=people, reports=reports)
    return templates.TemplateResponse(
        request=request,
        name='recap.html',
        context={'recap': recap},
    )
