const PERSON_DEFS = [
  ['drake', 'Drake', 'Executive lead', 'Founder mode', null],
  ['ricardo', 'Ricardo', 'Operations manager', 'Day shift', 'drake'],
  ['norman', 'Norman', 'Special projects', 'Day shift', 'drake'],
  ['cody', 'Cody', 'Outbound supervisor', '2nd shift', 'ricardo'],
  ['luis', 'Luis', 'Inbound supervisor', '2nd shift', 'ricardo'],
  ['adam', 'Adam', 'Inventory supervisor', 'Swing shift', 'ricardo'],
  ['nate', 'Nate', 'Floor lead', 'Closing shift', 'ricardo'],
  ['emily', 'Emily', 'Returns lead', 'Closing shift', 'ricardo'],
  ['ana', 'Ana', 'Packing lead', 'Night shift', 'cody'],
  ['danielle', 'Danielle', 'Shipping coordinator', 'Night shift', 'cody'],
  ['brenda', 'Brenda', 'Receiving lead', 'Night shift', 'luis'],
  ['ophelia', 'Ophelia', 'Dock coordinator', 'Night shift', 'luis'],
  ['remar', 'Remar', 'Unload lead', 'Night shift', 'luis'],
  ['edwin', 'Edwin', 'Cycle count lead', 'Swing shift', 'adam'],
  ['maria', 'Maria', 'Inventory control', 'Swing shift', 'adam'],
  ['maria-l', 'Maria L', 'Replenishment lead', 'Swing shift', 'adam'],
];

const DAY_KEYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];

function firstName(name) {
  return name.split(' ')[0];
}

function normalizeDays(days, cadence) {
  const normalized = Array.isArray(days)
    ? [...new Set(days.map((day) => String(day).trim().toLowerCase()).filter((day) => DAY_KEYS.includes(day)))]
    : [];

  if (normalized.length) return normalized;
  if (cadence === 'weekdays') return ['mon', 'tue', 'wed', 'thu', 'fri'];
  return [];
}

function assignmentAppliesOnDate(assignment, date = new Date()) {
  if (assignment.active === false) return false;

  const dayKey = DAY_KEYS[date.getDay()];
  switch (assignment.cadence) {
    case 'today':
    case 'daily':
      return true;
    case 'weekdays':
      return ['mon', 'tue', 'wed', 'thu', 'fri'].includes(dayKey);
    case 'custom':
      return assignment.days.includes(dayKey);
    default:
      return true;
  }
}

function defaultQuestionsFor(person) {
  const shortName = firstName(person.name);
  return [
    {
      id: `${person.id}-mood`,
      type: 'choice',
      source: 'default',
      prompt: `How are we doing, ${shortName}?`,
      helper: 'Pick the closest fit.',
      choices: ['Great', 'Good', 'Okay', 'Rough'],
    },
    {
      id: `${person.id}-wins`,
      type: 'textarea',
      source: 'default',
      prompt: 'What is the biggest thing that went right on your side today?',
      helper: 'Short and useful beats long and perfect.',
      placeholder: 'Example: dock cleared before cutoff',
    },
    {
      id: `${person.id}-risk`,
      type: 'text',
      source: 'default',
      prompt: 'What is the one thing leadership should watch tomorrow?',
      helper: 'Give the cleanest handoff note you can.',
      placeholder: 'Example: labor gap in picking after 3 PM',
    },
  ];
}

export const PEOPLE = PERSON_DEFS.map(([id, name, role, shift, managerId]) => ({
  id,
  name,
  role,
  shift,
  managerId,
  defaultQuestions: defaultQuestionsFor({ id, name }),
}));

export function buildOrgIndex(people) {
  const byId = new Map();
  const children = new Map();

  for (const person of people) {
    byId.set(person.id, person);
    children.set(person.id, []);
  }

  for (const person of people) {
    if (!person.managerId) continue;
    if (!children.has(person.managerId)) children.set(person.managerId, []);
    children.get(person.managerId).push(person.id);
  }

  return { byId, children };
}

export function getDescendantIds(orgIndex, personId) {
  const queue = [...(orgIndex.children.get(personId) || [])];
  const descendants = [];
  while (queue.length) {
    const current = queue.shift();
    descendants.push(current);
    queue.push(...(orgIndex.children.get(current) || []));
  }
  return descendants;
}

export function canAssignQuestions(orgIndex, personId) {
  return getDescendantIds(orgIndex, personId).length > 0;
}

export function getAssignablePeople(people, orgIndex, personId) {
  const ids = new Set(getDescendantIds(orgIndex, personId));
  if (personId === 'drake') ids.add(personId);
  return people.filter((person) => ids.has(person.id));
}

let nextAssignmentCounter = 1;

export function normalizeAssignment(input) {
  const prompt = String(input.prompt || '').trim();
  const type = input.type || 'text';
  const helper = String(input.helper || '').trim();
  const cadence = input.cadence || 'today';
  const options = Array.isArray(input.options)
    ? input.options.map((item) => String(item).trim()).filter(Boolean)
    : [];
  const days = normalizeDays(input.days, cadence);

  return {
    id: input.id || `assignment-${nextAssignmentCounter++}`,
    createdBy: input.createdBy,
    assignedTo: input.assignedTo,
    createdAt: input.createdAt || new Date().toISOString(),
    prompt,
    type,
    helper,
    cadence,
    days,
    active: input.active !== false,
    options,
    source: 'manager-assigned',
    placeholder: input.placeholder || '',
  };
}

export function mergeQuestionsForEmployee(person, assignments, date = new Date()) {
  const ownAssignments = assignments
    .filter((assignment) => assignment.assignedTo === person.id && assignmentAppliesOnDate(assignment, date))
    .map((assignment) => ({
      id: assignment.id,
      type: assignment.type,
      prompt: assignment.prompt,
      helper: assignment.helper,
      placeholder: assignment.placeholder,
      cadence: assignment.cadence,
      days: assignment.days,
      choices: ['choice', 'multi-select'].includes(assignment.type) ? assignment.options : undefined,
      source: 'manager-assigned',
    }));

  return [...person.defaultQuestions, ...ownAssignments];
}

export function assignmentTypeLabel(type) {
  switch (type) {
    case 'text': return 'Short answer';
    case 'textarea': return 'Long answer';
    case 'number': return 'Number';
    case 'choice': return 'Quick choice';
    case 'yesno': return 'Yes / No';
    default: return 'Answer';
  }
}
