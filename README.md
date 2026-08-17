# AI Job Description Generator & Customizer

A standalone AI-powered module that generates professional Job Descriptions from a few basic inputs, and lets you refine them with natural-language instructions. Built to be modular — designed so it can later be integrated into a larger ATS (Applicant Tracking System).

## Features

- Generate a complete, professional Job Description from 4 simple inputs: Job Title, Experience Required, Required Skills, and Employment Type
- Edit the generated JD directly, or refine it with a custom natural-language prompt (e.g. *"make this more concise and emphasize Python experience"*)
- Modify the JD as many times as needed
- Copy the final JD to clipboard
- Clean error handling, loading states, and input validation throughout

## Tech Stack

**Backend**
- FastAPI (Python)
- Layered architecture: Router → Service → LLM Integration
- LLM: Groq API (OpenAI-compatible), using `llama-3.3-70b-versatile`

**Frontend**
- React + Vite
- Plain fetch-based API layer, no extra state management library needed

## Project Structure

```
jd-generator/
├── backend/
│   ├── main.py                  # FastAPI app entrypoint
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── routers/jd.py        # API endpoints
│   │   ├── schemas/jd.py        # Request/response models (Pydantic)
│   │   ├── services/
│   │   │   ├── jd_service.py       # Prompt construction, business logic
│   │   │   └── openai_service.py   # LLM API client (Groq)
│   │   └── core/
│   │       ├── config.py           # Environment variable loading
│   │       └── exceptions.py       # Custom error types
│   └── tests/                   # Backend test suite
└── frontend/
    ├── src/
    │   ├── App.jsx               # Main component, owns app state
    │   ├── components/
    │   │   ├── JobInfoForm.jsx      # Input form
    │   │   ├── JDDisplay.jsx        # JD display + custom prompt UI
    │   │   └── ErrorBanner.jsx      # Error display
    │   └── services/
    │       └── jdApi.js          # Backend API calls
    └── vite.config.js
```

## API Endpoints

### `POST /api/jd/generate`
Generates a new Job Description.

**Request:**
```json
{
  "job_title": "Backend Developer",
  "experience_required": "2-3 years",
  "required_skills": ["Python", "FastAPI", "PostgreSQL"],
  "employment_type": "Full-time"
}
```

**Response:**
```json
{
  "success": true,
  "job_description": "..."
}
```

### `POST /api/jd/modify`
Modifies an existing Job Description based on a custom instruction.

**Request:**
```json
{
  "current_jd": "...",
  "custom_prompt": "Make it more concise and emphasize Python."
}
```

**Response:**
```json
{
  "success": true,
  "job_description": "..."
}
```

## Setup & Running Locally

### Prerequisites
- Python 3.11+
- Node.js 18+
- A free [Groq API key](https://console.groq.com)

### Backend

```bash
cd backend
cp .env.example .env
# Add your Groq API key to .env
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend runs at `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

Both need to be running at the same time for the app to work.

### Running Tests

```bash
cd backend
pytest tests/ -v
```

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your Groq API key |
| `OPENAI_MODEL` | Model name (default: `llama-3.3-70b-versatile`) |
| `REQUEST_TIMEOUT_SECONDS` | Timeout for LLM requests (default: `30`) |

## Design Notes

- **Scope:** This is intentionally a standalone module, not a full ATS — no database, authentication, resume parsing, or candidate management.
- **Provider-agnostic AI layer:** All LLM calls are isolated in `openai_service.py`, so switching providers (this project moved from OpenAI to Groq) requires changing only one file.
- **Validation-first:** Input validation happens before any AI call is made, preventing wasted requests on invalid data.
