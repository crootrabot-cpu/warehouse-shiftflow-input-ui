
const employees = [
  {
    id: 'marcus-hill',
    name: 'Marcus Hill',
    role: 'Outbound lead',
    shift: 'Day shift',
    questions: [
      { id: 'mood', type: 'choice', prompt: 'How are we doing, Marcus?', helper: 'Pick the closest fit.', choices: ['Great', 'Good', 'Okay', 'Rough'] },
      { id: 'trucks', type: 'number', prompt: 'How many late trucks are still open?', placeholder: '0', unit: 'trucks', helper: 'Numbers only.' },
      { id: 'blockers', type: 'textarea', prompt: 'Anything blocking outbound tonight?', placeholder: 'Short answer is fine.', helper: 'Mention anything that could hurt tomorrow.' },
      { id: 'cleanup', type: 'choice', prompt: 'Is cleanup fully closed?', choices: ['Yes, complete', 'Mostly complete', 'No, still open'], helper: 'Tap one and move on.' },
      { id: 'labor', type: 'text', prompt: 'What’s the biggest labor pressure right now?', placeholder: 'Example: picker coverage after 7 PM', helper: 'One clear issue is enough.' },
      { id: 'safety', type: 'yesno', prompt: 'Any safety issue we need to note before close?', helper: 'If yes, we can follow up in the dashboard.' }
    ]
  },
  {
    id: 'alina-ruiz',
    name: 'Alina Ruiz',
    role: 'Inbound supervisor',
    shift: '2nd shift',
    questions: [
      { id: 'mood', type: 'choice', prompt: 'How are we doing, Alina?', helper: 'Pick the closest fit.', choices: ['Great', 'Good', 'Okay', 'Rough'] },
      { id: 'receipts', type: 'number', prompt: 'How many receipts are still unposted?', placeholder: '0', unit: 'receipts', helper: 'Numbers only.' },
      { id: 'damage', type: 'yesno', prompt: 'Any damage issue that needs manager eyes?', helper: 'Answer yes or no.' },
      { id: 'dock', type: 'textarea', prompt: 'What needs attention on the dock before tomorrow?', placeholder: 'Short answer is fine.', helper: 'Think handoff notes, not a novel.' },
      { id: 'staffing', type: 'choice', prompt: 'How did staffing feel today?', choices: ['Fully covered', 'Tight but okay', 'Understaffed'], helper: 'Fast answer is best.' }
    ]
  },
  {
    id: 'devon-lee',
    name: 'Devon Lee',
    role: 'Inventory control',
    shift: 'Swing shift',
    questions: [
      { id: 'mood', type: 'choice', prompt: 'How are we doing, Devon?', helper: 'Pick the closest fit.', choices: ['Great', 'Good', 'Okay', 'Rough'] },
      { id: 'counts', type: 'number', prompt: 'How many cycle counts are still open?', placeholder: '0', unit: 'counts', helper: 'Numbers only.' },
      { id: 'variance', type: 'textarea', prompt: 'Any variance we should flag for leadership?', placeholder: 'Brief note', helper: 'Keep it sharp.' },
      { id: 'location-health', type: 'choice', prompt: 'How does location accuracy feel right now?', choices: ['Strong', 'Watch list', 'Needs work'], helper: 'Tap one.' },
      { id: 'followup', type: 'text', prompt: 'What is the one follow-up you want tomorrow morning?', placeholder: 'Example: verify zone B replenishment', helper: 'One item only.' }
    ]
  },
  {
    id: 'sara-nguyen',
    name: 'Sara Nguyen',
    role: 'Returns lead',
    shift: 'Closing shift',
    questions: [
      { id: 'mood', type: 'choice', prompt: 'How are we doing, Sara?', helper: 'Pick the closest fit.', choices: ['Great', 'Good', 'Okay', 'Rough'] },
      { id: 'backlog', type: 'number', prompt: 'How many returns are rolling to tomorrow?', placeholder: '0', unit: 'returns', helper: 'Numbers only.' },
      { id: 'priority', type: 'text', prompt: 'What should leadership pay attention to first thing tomorrow?', placeholder: 'Example: RTV queue aging', helper: 'Keep it crisp.' },
      { id: 'quality', type: 'yesno', prompt: 'Any quality issue that needs follow-up?', helper: 'Yes or no is enough.' }
    ]
  },
  {
    id: 'jamal-brooks',
    name: 'Jamal Brooks',
    role: 'Shipping coordinator',
    shift: 'Night shift',
    questions: [
      { id: 'mood', type: 'choice', prompt: 'How are we doing, Jamal?', helper: 'Pick the closest fit.', choices: ['Great', 'Good', 'Okay', 'Rough'] },
      { id: 'waves', type: 'number', prompt: 'How many shipping waves still need help?', placeholder: '0', unit: 'waves', helper: 'Numbers only.' },
      { id: 'carrier', type: 'textarea', prompt: 'Anything carrier-related that will hit tomorrow?', placeholder: 'Short answer is fine.', helper: 'Only what matters.' },
      { id: 'handoff', type: 'text', prompt: 'What’s the cleanest handoff note for first shift?', placeholder: 'One sentence', helper: 'Think useful, not perfect.' }
    ]
  },
  {
    id: 'priya-patel',
    name: 'Priya Patel',
    role: 'Quality assurance',
    shift: 'Mid shift',
    questions: [
      { id: 'mood', type: 'choice', prompt: 'How are we doing, Priya?', helper: 'Pick the closest fit.', choices: ['Great', 'Good', 'Okay', 'Rough'] },
      { id: 'holds', type: 'number', prompt: 'How many quality holds are still open?', placeholder: '0', unit: 'holds', helper: 'Numbers only.' },
      { id: 'risk', type: 'choice', prompt: 'What’s the overall quality risk level tonight?', choices: ['Low', 'Medium', 'High'], helper: 'Choose the best fit.' },
      { id: 'details', type: 'textarea', prompt: 'Anything specific leadership should know?', placeholder: 'Add a concise note', helper: 'Short and direct wins.' }
    ]
  }
];

const state = {
  employee: null,
  currentIndex: 0,
  answers: [],
  screen: 'picker'
};

const pickerScreen = document.getElementById('pickerScreen');
const chatScreen = document.getElementById('chatScreen');
const completeScreen = document.getElementById('completeScreen');
const nameGrid = document.getElementById('nameGrid');
const nameSearch = document.getElementById('nameSearch');
const peopleCount = document.getElementById('peopleCount');
const currentDate = document.getElementById('currentDate');
const sidebarName = document.getElementById('sidebarName');
const sidebarShift = document.getElementById('sidebarShift');
const progressText = document.getElementById('progressText');
const progressFill = document.getElementById('progressFill');
const chatTitle = document.getElementById('chatTitle');
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

function formatDate() {
  return new Date().toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' });
}

function setScreen(screen) {
  state.screen = screen;
  pickerScreen.classList.toggle('active', screen === 'picker');
  chatScreen.classList.toggle('active', screen === 'chat');
  completeScreen.classList.toggle('active', screen === 'complete');
}

function renderNames(filter = '') {
  const q = filter.trim().toLowerCase();
  const filtered = employees.filter((employee) => {
    return employee.name.toLowerCase().includes(q) || employee.role.toLowerCase().includes(q);
  });
  peopleCount.textContent = `${filtered.length} ${filtered.length === 1 ? 'person' : 'people'}`;
  nameGrid.innerHTML = filtered.map((employee) => `
    <button class="name-card" data-employee-id="${employee.id}">
      <div>
        <strong>${employee.name}</strong>
        <p>${employee.role}</p>
      </div>
      <span class="question-count">${employee.questions.length} assigned questions • ${employee.shift}</span>
    </button>
  `).join('');

  nameGrid.querySelectorAll('.name-card').forEach((card) => {
    card.addEventListener('click', () => {
      const employee = employees.find((item) => item.id === card.dataset.employeeId);
      startSession(employee);
    });
  });
}

function startSession(employee) {
  state.employee = employee;
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
  return state.employee?.questions[state.currentIndex] || null;
}

function labelForType(type) {
  switch (type) {
    case 'choice': return 'Quick choice';
    case 'number': return 'Number';
    case 'textarea': return 'Long answer';
    case 'text': return 'Short answer';
    case 'yesno': return 'Yes / No';
    default: return 'Answer';
  }
}

function updateProgress() {
  const total = state.employee.questions.length;
  const currentDisplay = Math.min(state.currentIndex + 1, total);
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

  questionTypeBadge.textContent = labelForType(question.type);
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
    question.choices.forEach((choice) => {
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
    addBotMessage(question.prompt, question.helper || 'Assigned prompt');
  }

  if (showTextInput) {
    answerInput.focus();
  }
}

function submitAnswer(rawValue) {
  const question = getCurrentQuestion();
  if (!question) return;

  let value = (rawValue ?? answerInput.value).trim();
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
  progressFill.style.width = `${(state.answers.length / state.employee.questions.length) * 100}%`;
  saveStatus.textContent = 'Captured';

  setTimeout(() => {
    renderQuestion();
  }, 140);
}

function finishSession() {
  progressText.textContent = `${state.employee.questions.length} of ${state.employee.questions.length}`;
  progressFill.style.width = '100%';
  addBotMessage(`That’s everything — thanks, ${state.employee.name.split(' ')[0]} 👊`, 'Complete');
  completeTitle.textContent = `Have a good rest of your day, ${state.employee.name.split(' ')[0]}.`;
  completeSummary.textContent = `You answered ${state.employee.questions.length} assigned questions with almost no busy work. This is the clean intake surface we’d wire to Apps Script next.`;
  setTimeout(() => setScreen('complete'), 420);
}

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

nameSearch.addEventListener('input', (event) => renderNames(event.target.value));
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
  const employee = employees.find((item) => item.id === employeeId);
  if (!employee) return;
  startSession(employee);
}

currentDate.textContent = formatDate();
renderNames();
bootFromUrl();
