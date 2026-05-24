import test from 'node:test';
import assert from 'node:assert/strict';

import {
  PEOPLE,
  buildOrgIndex,
  canAssignQuestions,
  getAssignablePeople,
  mergeQuestionsForEmployee,
  normalizeAssignment,
} from '../assets/shiftflow-state.mjs';

const orgIndex = buildOrgIndex(PEOPLE);

test('Drake can assign to himself and every descendant in the org tree', () => {
  const names = getAssignablePeople(PEOPLE, orgIndex, 'drake').map((person) => person.name);
  assert.deepEqual(names, [
    'Drake',
    'Ricardo',
    'Norman',
    'Cody',
    'Luis',
    'Adam',
    'Nate',
    'Emily',
    'Ana',
    'Danielle',
    'Brenda',
    'Ophelia',
    'Remar',
    'Edwin',
    'Maria',
    'Maria L',
  ]);
});

test('Ricardo can only assign inside his subtree', () => {
  const names = getAssignablePeople(PEOPLE, orgIndex, 'ricardo').map((person) => person.name);
  assert.deepEqual(names, [
    'Cody',
    'Luis',
    'Adam',
    'Nate',
    'Emily',
    'Ana',
    'Danielle',
    'Brenda',
    'Ophelia',
    'Remar',
    'Edwin',
    'Maria',
    'Maria L',
  ]);
});

test('individual contributors cannot assign questions', () => {
  assert.equal(canAssignQuestions(orgIndex, 'emily'), false);
  assert.equal(canAssignQuestions(orgIndex, 'norman'), false);
});

test('merged report questions include manager-assigned questions after defaults', () => {
  const merged = mergeQuestionsForEmployee(
    PEOPLE.find((person) => person.id === 'cody'),
    [
      normalizeAssignment({
        id: 'q-1',
        createdBy: 'ricardo',
        assignedTo: 'cody',
        prompt: 'What is the one thing leadership should unblock tomorrow?',
        type: 'textarea',
        helper: 'Keep it direct.',
        cadence: 'today',
      }),
    ],
  );

  assert.equal(merged.at(-1).prompt, 'What is the one thing leadership should unblock tomorrow?');
  assert.equal(merged.at(-1).source, 'manager-assigned');
  assert.equal(merged[0].source, 'default');
});

test('custom-day assignments only appear on configured days', () => {
  const person = PEOPLE.find((item) => item.id === 'ana');
  const assignments = [
    normalizeAssignment({
      id: 'q-custom',
      createdBy: 'cody',
      assignedTo: 'ana',
      prompt: 'What machine issue needs to be watched on packout?',
      type: 'text',
      cadence: 'custom',
      days: ['mon', 'wed'],
    }),
  ];

  const wednesday = mergeQuestionsForEmployee(person, assignments, new Date('2026-05-27T12:00:00Z'));
  const thursday = mergeQuestionsForEmployee(person, assignments, new Date('2026-05-28T12:00:00Z'));

  assert.equal(wednesday.some((question) => question.id === 'q-custom'), true);
  assert.equal(thursday.some((question) => question.id === 'q-custom'), false);
});
