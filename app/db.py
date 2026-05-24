from __future__ import annotations

import sqlite3
from pathlib import Path


def connect(db_path: str | Path) -> sqlite3.Connection:
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    return connection


def init_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        '''
        CREATE TABLE IF NOT EXISTS people (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            team TEXT NOT NULL,
            manager_id TEXT REFERENCES people(id),
            can_assign INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL REFERENCES people(id),
            report_date TEXT NOT NULL,
            submitted_at TEXT NOT NULL,
            status TEXT NOT NULL,
            summary_text TEXT NOT NULL DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS report_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL REFERENCES reports(id) ON DELETE CASCADE,
            question_key TEXT NOT NULL,
            question_text TEXT NOT NULL,
            answer_value TEXT NOT NULL,
            answer_type TEXT NOT NULL,
            source TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS question_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_by_person_id TEXT NOT NULL REFERENCES people(id),
            assigned_to_person_id TEXT NOT NULL REFERENCES people(id),
            prompt TEXT NOT NULL,
            answer_type TEXT NOT NULL,
            helper_text TEXT NOT NULL DEFAULT '',
            placeholder TEXT NOT NULL DEFAULT '',
            options_json TEXT NOT NULL DEFAULT '[]',
            cadence TEXT NOT NULL DEFAULT 'today',
            days_json TEXT NOT NULL DEFAULT '[]',
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_reports_report_date ON reports(report_date);
        CREATE INDEX IF NOT EXISTS idx_reports_person_id ON reports(person_id);
        CREATE INDEX IF NOT EXISTS idx_report_answers_report_id ON report_answers(report_id);
        CREATE INDEX IF NOT EXISTS idx_assignments_assigned_to_person_id ON question_assignments(assigned_to_person_id);
        '''
    )
    connection.commit()
