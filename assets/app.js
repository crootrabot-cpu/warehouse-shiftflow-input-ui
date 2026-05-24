import {
  PEOPLE,
  assignmentTypeLabel,
  buildOrgIndex,
  canAssignQuestions,
  getAssignablePeople,
  mergeQuestionsForEmployee,
  normalizeAssignment,
} from './shiftflow-state.mjs';

const STORAGE_KEY = 'shiftflow-manager-assignments-v1';
const DAY_LABELS = {
  mon: 'Mon',
  tue: 'Tue',
  wed: 'Wed',
  thu: 'Thu',
  fri: 'Fri',
  sat: 'Sat',
  sun: 'Sun',
};

const orgIndex = buildOrgIndex(PEOPLE);

const state = {
  employee: null,
  sessionQuestions: [],
  currentIndex: 0,
  answers: [],
  screen: 'picker',
  mode: 'report',
  assignments: loadAssignments(),
  selectedManagerId: null,
  search: '',
  customDays: new Set(['mon', 'tue', 'wed', 'thu', 'fri']),
};

const pickerScreen = document.getElementById('pickerScreen');
const chatScreen = document.getElementById('chatScreen');
const completeScreen = document.getElementById('completeScreen');
const reportModeButton = document.getElementById('reportModeButton');
const assignModeButton = document.getElementById('assignModeButton');
const pickerTitle = document.getElementById('pickerTitle');
const pickerLede = document.getElementById('pickerLede');
const nameGrid = document.getElementById('nameGrid');
const nameSearch = document.getElementById('nameSearch');
const peopleCount = document.getElementById('peopleCount');
const peopleSummaryLabel = document.getElementById('peopleSummaryLabel');
const currentDate = document.getElementById('currentDate');

const builderEmpty = document.getElementById('builderEmpty');
const builderContent = document.getElementById('builderContent');
const builderEmptyTitle = document.getElementById('builderEmptyTitle');
const builderEmptyCopy = document.getElementById('builderEmptyCopy');
const builderTitle = document.getElementById('builderTitle');
const builderLead = document.getElementById('builderLead');
const builderScopeCount = document.getElementById('builderScopeCount');
const managerScope = document.getElementById('managerScope');
const assignmentForm = document.getElementById('assignmentForm');
const assignmentTarget = document.getElementById('assignmentTarget');
const assignmentType = document.getElementById('assignmentType');
const assignmentCadence = document.getElementById('assignmentCadence');
const customDaysShell = document.getElementById('customDaysShell');
const customDaysGrid = document.getElementById('customDaysGrid');
const assignmentPrompt = document.getElementById('assignmentPrompt');
const assignmentHelper = document.getElementById('assignmentHelper');
const assignmentPlaceholder = document.getElementById('assignmentPlaceholder');
const assignmentOptionsShell = document.getElementById('assignmentOptionsShell');
const assignmentOptions = document.getElementById('assignmentOptions');
const targetPreview = document.getElementById('targetPreview');
const assignmentSubmitButton = document.getElementById('assignmentSubmitButton');
const builderStatus = document.getElementById('builderStatus');
const assignmentList = document.getElementById('assignmentList');
const assignmentListSummary = document.getElementById('assignmentListSummary');

const sidebarName = document.getElementById('sidebarName');
const sidebarShift = document.getElementById('sidebarShift');
const progressText = document.getElementById('progressText');
const progressFill = document.getElementById('progressFill');
const chatTitle = document.getElementById('chatTitle');
const questionSourceBadge = document.getElementById('questionSourceBadge');
const questionTypeBadge = document.getElementById('questionTypeBadge');
const transcript = document.getElementById('transcript');
const quickReplies = document.getElementById('quickReplies');
const textInputShell = document.getElementById('textInputShell');
const answerInput = document.getElementById('answerInput');
const unitLabel = document.getElementById('unitLabel');
const helperText = document.getElementById('helperText');
const saveStatus = document.getElementById('saveStatus');
const composerForm = document.getElementById('composerForm');
const submitButton = document.getElementById('submitButton');
const completeTitle = document.getElementById('completeTitle');
const completeSummary = document.getElementById('completeSummary');
const changePersonButton = document.getElementById('changePersonButton');
const restartButton = document.getElementById('restartButton');
const reviewAnswersButton = document.getElementById('reviewAnswersButton');

function loadAssignments() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.map((item) => normalizeAssignment(item)) : [];
  } catch {
    return [];
  }
}

function saveAssignments() {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state.assignments));
}

function formatDate() {
  return new Date().toLocaleDateString(undefined, {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  });
}

function getEmployee(employeeId) {
  return PEOPLE.find((person) => person.id === employeeId) || null;
}

function getQuestionsForEmployee(employee, date = new Date()) {
  return mergeQuestionsForEmployee(employee, state.assignments, date);
}

function getQuestionCount(employee) {
  return getQuestionsForEmployee(employee).length;
}

function setScreen(screen) {
  state.screen = screen;
  pickerScreen.classList.toggle('active', screen === 'picker');
  chatScreen.classList.toggle('active', screen === 'chat');
  completeScreen.classList.toggle('active', screen === 'complete');
}

function setMode(mode) {
  state.mode = mode;
  reportModeButton.classList.toggle('active', mode === 'report');
  assignModeButton.classList.toggle('active', mode === 'assign');
  reportModeButton.setAttribute('aria-pressed', String(mode === 'report'));
  assignModeButton.setAttribute('aria-pressed', String(mode === 'assign'));

  if (mode === 'report') {
    pickerTitle.textContent = 'Who’s checking out today?';
    pickerLede.textContent = 'No dashboards. No forms. Just tap your name and answer the questions that matter.';
    peopleSummaryLabel.textContent = 'Assigned questions ready';
    nameSearch.placeholder = 'Search your name';
    builderEmptyTitle.textContent = 'Ask better follow-up questions.';
    builderEmptyCopy.innerHTML = 'Switch to <strong>Ask a question</strong>, pick a manager, and build a lightweight prompt that drops straight into that person’s end-of-day flow.';
  } else {
    pickerTitle.textContent = 'Who needs to ask something?';
    pickerLede.textContent = 'Pick a manager, assign a clean follow-up, and make it land in the right person’s report without adding a second tool.';
    peopleSummaryLabel.textContent = 'Manager permissions enforced';
    nameSearch.placeholder = 'Search manager or team';
    builderEmptyTitle.textContent = 'Pick a manager on the left.';
    builderEmptyCopy.innerHTML = 'Only people with reports can assign questions. Once you pick one, the builder will only show the people they’re allowed to ask.';
  }

  renderNames(state.search);
  renderBuilder();
}

function renderNames(filter = state.search) {
  state.search = filter;
  const query = filter.trim().toLowerCase();
  const filtered = PEOPLE.filter((person) => {
    return person.name.toLowerCase().includes(query) || person.role.toLowerCase().includes(query);
  });

  peopleCount.textContent = `${filtered.length} ${filtered.length === 1 ? 'person' : 'people'}`;

  nameGrid.innerHTML = filtered.map((person) => {
    if (state.mode === 'report') {
      return `
        <button class="name-card" data-employee-id="${person.id}">
          <div>
            <strong>${person.name}</strong>
            <p>${person.role}</p>
          </div>
          <span class="question-count">${getQuestionCount(person)} questions • ${person.shift}</span>
        </button>
      `;
    }

    const allowed = canAssignQuestions(orgIndex, person.id);
    const scopeCount = allowed ? getAssignablePeople(PEOPLE, orgIndex, person.id).length : 0;
    const classes = ['name-card', 'manager-card'];
    if (!allowed) classes.push('disabled');
    if (state.selectedManagerId === person.id) classes.push('selected');

    return `
      <button class="${classes.join(' ')}" data-employee-id="${person.id}" ${allowed ? '' : 'disabled'}>
        <div>
          <strong>${person.name}</strong>
          <p>${person.role}</p>
        </div>
        <span class="question-count">${allowed ? `${scopeCount} people you can ask` : 'No reports to assign to'}</span>
      </button>
    `;
  }).join('');

  if (!filtered.length) {
    nameGrid.innerHTML = '<div class="empty-grid-state">No matches. Try a different name or role.</div>';
    return;
  }

  nameGrid.querySelectorAll('.name-card').forEach((card) => {
    card.addEventListener('click', () => {
      const employee = getEmployee(card.dataset.employeeId);
      if (!employee) return;

      if (state.mode === 'report') {
        startSession(employee);
        return;
      }

      if (!canAssignQuestions(orgIndex, employee.id)) return;
      state.selectedManagerId = employee.id;
      builderStatus.textContent = 'Local prototype only';
      renderNames(state.search);
      renderBuilder();
    });
  });
}

function renderBuilder() {
  if (state.mode === 'report') {
    builderEmpty.classList.remove('hidden');
    builderContent.classList.add('hidden');
    return;
  }

  const manager = getEmployee(state.selectedManagerId);
  if (!manager) {
    builderEmpty.classList.remove('hidden');
    builderContent.classList.add('hidden');
    return;
  }

  builderEmpty.classList.add('hidden');
  builderContent.classList.remove('hidden');

  const assignablePeople = getAssignablePeople(PEOPLE, orgIndex, manager.id);
  builderTitle.textContent = `${manager.name} can ask these people`;
  builderLead.textContent = `${manager.role} • keep it light, specific, and actually useful at close-out.`;
  builderScopeCount.textContent = `${assignablePeople.length} ${assignablePeople.length === 1 ? 'person' : 'people'}`;
  managerScope.innerHTML = assignablePeople.map((person) => `<span class="scope-chip">${person.name}</span>`).join('');

  const currentTargetStillValid = assignablePeople.some((person) => person.id === assignmentTarget.value);
  if (!currentTargetStillValid) {
    assignmentTarget.innerHTML = assignablePeople.map((person) => `<option value="${person.id}">${person.name} • ${person.role}</option>`).join('');
  } else {
    const priorValue = assignmentTarget.value;
    assignmentTarget.innerHTML = assignablePeople.map((person) => `<option value="${person.id}">${person.name} • ${person.role}</option>`).join('');
    assignmentTarget.value = priorValue;
  }

  if (!assignmentTarget.value && assignablePeople[0]) {
    assignmentTarget.value = assignablePeople[0].id;
  }

  renderAssignmentControls();
  renderTargetPreview();
  renderAssignedList();
}

function renderAssignmentControls() {
  const showOptions = assignmentType.value === 'choice';
  const showCustomDays = assignmentCadence.value === 'custom';
  assignmentOptionsShell.classList.toggle('hidden', !showOptions);
  customDaysShell.classList.toggle('hidden', !showCustomDays);

  customDaysGrid.querySelectorAll('.day-chip').forEach((button) => {
    button.classList.toggle('active', state.customDays.has(button.dataset.day));
    button.setAttribute('aria-pressed', String(state.customDays.has(button.dataset.day)));
  });
}

function cadenceLabel(assignment) {
  if (assignment.cadence === 'daily') return 'Every day';
  if (assignment.cadence === 'weekdays') return 'Weekdays';
  if (assignment.cadence === 'custom') {
    return assignment.days.length ? assignment.days.map((day) => DAY_LABELS[day]).join(', ') : 'Custom';
  }
  return 'Today only';
}

function renderAssignedList() {
  const manager = getEmployee(state.selectedManagerId);
  if (!manager) {
    assignmentList.innerHTML = '';
    assignmentListSummary.textContent = 'Nothing assigned yet.';
    return;
  }

  const items = state.assignments
    .filter((assignment) => assignment.createdBy === manager.id && assignment.active !== false)
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

  assignmentListSummary.textContent = items.length
    ? `${items.length} active ${items.length === 1 ? 'question' : 'questions'}`
    : 'Nothing assigned yet.';

  assignmentList.innerHTML = items.length
    ? items.map((assignment) => {
      const target = getEmployee(assignment.assignedTo);
      const extra = assignment.type === 'choice' && assignment.options.length
        ? `<div class="assignment-options">${assignment.options.map((option) => `<span>${option}</span>`).join('')}</div>`
        : '';

      return `
        <article class="assignment-card">
          <div class="assignment-card-top">
            <span class="meta-pill subdued">${target?.name || 'Unknown target'}</span>
            <span class="meta-pill subdued">${cadenceLabel(assignment)}</span>
          </div>
          <h4>${assignment.prompt}</h4>
          <p>${assignment.helper || assignment.placeholder || 'No helper copy added.'}</p>
          <div class="assignment-card-meta">
            <span>${assignmentTypeLabel(assignment.type)}</span>
            <span>Added ${new Date(assignment.createdAt).toLocaleDateString()}</span>
          </div>
          ${extra}
        </article>
      `;
    }).join('')
    : '<div class="assignment-empty">No assigned questions yet. Add one and it will appear here.</div>';
}

function renderTargetPreview() {
  const target = getEmployee(assignmentTarget.value);
  if (!target) {
    targetPreview.textContent = 'Pick a target to preview the report flow impact.';
    return;
  }

  const existingCount = getQuestionsForEmployee(target).length;
  const suffix = assignmentCadence.value === 'custom'
    ? `on ${[...state.customDays].map((day) => DAY_LABELS[day]).join(', ') || 'selected days'}`
    : cadenceLabel({ cadence: assignmentCadence.value, days: [...state.customDays] });

  targetPreview.textContent = `${target.name} currently sees ${existingCount} questions. This new one will be appended after the defaults and show ${suffix.toLowerCase()}.`;
}

function parseOptions() {
  return assignmentOptions.value
    .split(/\n|,/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function resetAssignmentForm() {
  assignmentType.value = 'text';
  assignmentCadence.value = 'today';
  assignmentPrompt.value = '';
  assignmentHelper.value = '';
  assignmentPlaceholder.value = '';
  assignmentOptions.value = '';
  state.customDays = new Set(['mon', 'tue', 'wed', 'thu', 'fri']);
  renderAssignmentControls();
  renderTargetPreview();
}

function startSession(employee) {
  state.employee = employee;
  state.sessionQuestions = getQuestionsForEmployee(employee);
  state.currentIndex = 0;
  state.answers = [];
  sidebarName.textContent = employee.name;
  sidebarShift.textContent = `${employee.role} • ${employee.shift}`;
  chatTitle.textContent = 'End-of-day check-out';
  transcript.innerHTML = '';
  setScreen('chat');
  renderQuestion();
}

function getCurrentQuestion() {
  return state.sessionQuestions[state.currentIndex] || null;
}

function updateProgress() {
  const total = state.sessionQuestions.length;
  progressText.textContent = `${Math.min(state.answers.length + 1, total)} of ${total}`;
  const pct = total ? (state.answers.length / total) * 100 : 0;
  progressFill.style.width = `${pct}%`;
}

function addBotMessage(text, meta = 'Assigned prompt') {
  const row = document.createElement('div');
  row.className = 'message-row bot';
  row.innerHTML = `<div class="message-bubble"><span class="message-label">ShiftFlow</span><p class="message-text"></p><div class="message-meta">${meta}</div></div>`;
  row.querySelector('.message-text').textContent = text;
  transcript.appendChild(row);
  transcript.scrollTop = transcript.scrollHeight;
}

function addUserMessage(text) {
  const row = document.createElement('div');
  row.className = 'message-row user';
  row.innerHTML = `<div class="message-bubble"><span class="message-label">${state.employee.name}</span><p class="message-text"></p><div class="message-meta">Captured</div></div>`;
  row.querySelector('.message-text').textContent = text;
  transcript.appendChild(row);
  transcript.scrollTop = transcript.scrollHeight;
}

function autosizeTextarea() {
  answerInput.style.height = 'auto';
  answerInput.style.height = `${Math.min(answerInput.scrollHeight, 180)}px`;
}

function renderQuestion() {
  const question = getCurrentQuestion();
  updateProgress();

  if (!question) {
    finishSession();
    return;
  }

  questionTypeBadge.textContent = assignmentTypeLabel(question.type);
  questionSourceBadge.textContent = question.source === 'manager-assigned' ? 'Manager follow-up' : 'Default flow';
  helperText.textContent = question.helper || 'Press Enter to continue';
  saveStatus.textContent = 'Local prototype only';
  quickReplies.innerHTML = '';
  answerInput.value = '';
  answerInput.placeholder = question.placeholder || 'Type your answer';
  unitLabel.textContent = question.unit || '';
  autosizeTextarea();

  const showTextInput = !['choice', 'yesno'].includes(question.type);
  textInputShell.classList.toggle('hidden', !showTextInput);
  submitButton.classList.toggle('hidden', !showTextInput);
  answerInput.disabled = !showTextInput;

  if (question.type === 'choice') {
    (question.choices || []).forEach((choice) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'quick-reply';
      button.textContent = choice;
      button.addEventListener('click', () => submitAnswer(choice));
      quickReplies.appendChild(button);
    });
  }

  if (question.type === 'yesno') {
    ['Yes', 'No'].forEach((choice) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'quick-reply';
      button.textContent = choice;
      button.addEventListener('click', () => submitAnswer(choice));
      quickReplies.appendChild(button);
    });
  }

  if (state.currentIndex > 0 || transcript.children.length === 0) {
    addBotMessage(question.prompt, question.source === 'manager-assigned' ? 'Manager-added prompt' : 'Default prompt');
  }

  if (showTextInput) {
    answerInput.focus();
  }
}

function submitAnswer(rawValue) {
  const question = getCurrentQuestion();
  if (!question) return;

  const value = String(rawValue ?? answerInput.value).trim();
  if (!value) {
    saveStatus.textContent = 'Answer required';
    return;
  }

  if (question.type === 'number' && Number.isNaN(Number(value))) {
    saveStatus.textContent = 'Use a number';
    return;
  }

  addUserMessage(value);
  state.answers.push({ questionId: question.id, prompt: question.prompt, value, type: question.type });
  state.currentIndex += 1;
  saveStatus.textContent = 'Captured';

  window.setTimeout(() => {
    renderQuestion();
  }, 140);
}

function finishSession() {
  const total = state.sessionQuestions.length;
  progressText.textContent = `${total} of ${total}`;
  progressFill.style.width = '100%';
  addBotMessage(`That’s everything — thanks, ${state.employee.name.split(' ')[0]} 👊`, 'Complete');
  completeTitle.textContent = `Have a good rest of your day, ${state.employee.name.split(' ')[0]}.`;
  completeSummary.textContent = `You answered ${total} questions, including any manager follow-ups that mattered today. This is the clean intake surface we’d wire to Apps Script next.`;
  window.setTimeout(() => setScreen('complete'), 420);
}

assignmentForm.addEventListener('submit', (event) => {
  event.preventDefault();

  const manager = getEmployee(state.selectedManagerId);
  const target = getEmployee(assignmentTarget.value);
  if (!manager || !target) {
    builderStatus.textContent = 'Pick a valid manager and target';
    return;
  }

  const prompt = assignmentPrompt.value.trim();
  if (!prompt) {
    builderStatus.textContent = 'Question prompt is required';
    assignmentPrompt.focus();
    return;
  }

  const options = assignmentType.value === 'choice' ? parseOptions() : [];
  if (assignmentType.value === 'choice' && options.length < 2) {
    builderStatus.textContent = 'Choice questions need at least 2 options';
    assignmentOptions.focus();
    return;
  }

  if (assignmentCadence.value === 'custom' && !state.customDays.size) {
    builderStatus.textContent = 'Pick at least one custom day';
    return;
  }

  const assignment = normalizeAssignment({
    createdBy: manager.id,
    assignedTo: target.id,
    prompt,
    type: assignmentType.value,
    helper: assignmentHelper.value,
    cadence: assignmentCadence.value,
    days: [...state.customDays],
    options,
    placeholder: assignmentPlaceholder.value,
  });

  state.assignments.push(assignment);
  saveAssignments();
  builderStatus.textContent = `Added for ${target.name}`;
  resetAssignmentForm();
  renderNames(state.search);
  renderBuilder();
});

composerForm.addEventListener('submit', (event) => {
  event.preventDefault();
  submitAnswer();
});

answerInput.addEventListener('input', autosizeTextarea);
answerInput.addEventListener('keydown', (event) => {
  const question = getCurrentQuestion();
  if (!question) return;
  const multiline = question.type === 'textarea';
  if (event.key === 'Enter' && (!multiline || !event.shiftKey)) {
    event.preventDefault();
    submitAnswer();
  }
});

nameSearch.addEventListener('input', (event) => {
  renderNames(event.target.value);
});

reportModeButton.addEventListener('click', () => setMode('report'));
assignModeButton.addEventListener('click', () => setMode('assign'));
assignmentType.addEventListener('change', () => {
  renderAssignmentControls();
});
assignmentCadence.addEventListener('change', () => {
  renderAssignmentControls();
  renderTargetPreview();
});
assignmentTarget.addEventListener('change', renderTargetPreview);
assignmentPrompt.addEventListener('input', renderTargetPreview);
customDaysGrid.querySelectorAll('.day-chip').forEach((button) => {
  button.addEventListener('click', () => {
    const day = button.dataset.day;
    if (state.customDays.has(day)) {
      state.customDays.delete(day);
    } else {
      state.customDays.add(day);
    }
    renderAssignmentControls();
    renderTargetPreview();
  });
});

changePersonButton.addEventListener('click', () => setScreen('picker'));
restartButton.addEventListener('click', () => setScreen('picker'));
reviewAnswersButton.addEventListener('click', () => {
  setScreen('chat');
  transcript.scrollTop = transcript.scrollHeight;
});

function bootFromUrl() {
  const params = new URLSearchParams(window.location.search);
  const employeeId = params.get('employee');
  if (!employeeId) return;
  const employee = getEmployee(employeeId);
  if (!employee) return;
  startSession(employee);
}

currentDate.textContent = formatDate();
renderAssignmentControls();
setMode('report');
bootFromUrl();
