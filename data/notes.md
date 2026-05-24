# Integration Notes

## Apps Script direction

This front-end should eventually read from and write to an Apps Script web app.

### Suggested contract

#### GET roster and questions
`GET /exec?action=session-config`

Returns:
```json
{
  "employees": [
    {
      "id": "marcus-hill",
      "name": "Marcus Hill",
      "role": "Outbound lead",
      "shift": "Day shift",
      "questions": [
        {
          "id": "mood",
          "type": "choice",
          "prompt": "How are we doing, Marcus?",
          "choices": ["Great", "Good", "Okay", "Rough"]
        }
      ]
    }
  ]
}
```

#### POST answer
`POST /exec?action=submit-answer`

Payload:
```json
{
  "employeeId": "marcus-hill",
  "questionId": "mood",
  "answer": "Good",
  "answeredAt": "2026-05-23T18:15:00Z"
}
```

#### POST complete session
`POST /exec?action=complete-session`

Payload:
```json
{
  "employeeId": "marcus-hill",
  "answers": []
}
```

## UX rule

Keep the conversational UI decoupled from the backend contract so we can swap Apps Script or migrate to another backend later.
