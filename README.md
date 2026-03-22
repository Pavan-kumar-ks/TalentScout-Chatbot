# TalentScout AI Hiring Assistant

AI-powered conversational hiring assistant built with Streamlit and Groq models.

The app collects candidate profile details, runs a structured technical interview, evaluates answers, asks follow-up questions, and stores interview outcomes in JSON.

## Table of Contents
- Live Demo
- Project Overview
- Key Capabilities
- End-to-End Workflow
- Architecture and Codebase
- Installation Instructions
- Configuration (.env)
- Usage Guide
- Technical Details
- Prompt Design
- Challenges and Solutions
- Data Storage Schema
- Performance Notes
- Troubleshooting
- Future Improvements

## Live Demo
- Production URL: https://talentscout-chatbot-zt7o.onrender.com/
- Hosting Platform: Render (Free Tier)

## Project Overview
TalentScout is a multi-language technical interview chatbot designed for recruiter and screening workflows.

Core idea:
- Keep interview logic and scoring canonical in English.
- Let candidates interact in their preferred language.
- Translate assistant output to the selected language.
- Persist candidate records in `data/candidates.json` with normalized English fields.

This architecture improves consistency, reduces scoring drift, and keeps stored data clean for downstream analysis.

## Key Capabilities
- Guided candidate onboarding:
  - Name, email, phone, experience, role, location, tech stack.
- Adaptive technical interview:
  - Generates 4 scenario-based questions with increasing difficulty.
- Strict answer evaluation:
  - Score + relevance + short actionable feedback.
- Follow-up generation:
  - One concise follow-up question focused on answer gaps.
- Multilingual candidate experience:
  - 10 language options in UI.
- Canonical English pipeline:
  - Input normalized to English for internal processing.
- Persistent storage:
  - Candidate data plus final score saved to JSON.

## End-to-End Workflow
1. Candidate selects interview language in UI.
2. Chatbot starts guided profile collection.
3. Candidate responses are translated to English internally when needed.
4. Technical questions are generated in English using LLaMA.
5. Candidate answers are evaluated in English using strict rubric.
6. Follow-up question is generated in English.
7. Final assistant message is translated once to selected language for display.
8. Candidate record is saved to `data/candidates.json` with both original and normalized English fields.

## Architecture and Codebase

### High-level modules
- `app.py`:
  - Streamlit UI, language selector, chat rendering, UI localization cache.
- `config.py`:
  - Environment config for interview model and translation model.
- `chatbot/`:
  - `state_manager.py`: main interview state machine and flow control.
  - `prompt_engine.py`: question-generation prompt template.
  - `question_generator.py`: runs prompt + parses numbered questions.
  - `evaluator.py`: strict technical evaluation prompt.
  - `followup_generator.py`: concise follow-up prompt.
  - `llm_handler.py`: Groq API call wrapper for interview LLM.
- `utils/`:
  - `translator.py`: translation functions, caching, translation-model API path.
  - `validators.py`: email and phone validation.
  - `helpers.py`: weak-answer detection.
  - `sentiment.py`: lightweight sentiment cue checks.
  - `data_handler.py`: JSON read/append/write persistence.
- `data/candidates.json`:
  - Candidate interview records.

### Model split (important)
- Interview and question generation model:
  - `GROQ_MODEL` (default: `llama-3.1-8b-instant`)
- Translation model:
  - `TRANSLATION_MODEL` (default: `openai/gpt-oss-120b`)

This split keeps technical reasoning fast while using a stronger multilingual model for translation quality.

## Installation Instructions

### Prerequisites
- Python 3.10+ recommended.
- Pip and virtual environment support.
- Groq API keys.

### 1) Clone repository
```bash
git clone <your-repo-url>
cd TalentScout-Chatbot
```

### 2) Create and activate virtual environment
Windows PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Create `.env`
Create a `.env` file in project root.

Required variables:
```env
GROQ_API_KEY=your_interview_flow_key
TRANSLATION_GROQ_API_KEY=your_translation_key
```

Optional variables:
```env
GROQ_MODEL=llama-3.1-8b-instant
GROQ_TIMEOUT_SECONDS=30
TRANSLATION_MODEL=openai/gpt-oss-120b
TRANSLATION_TIMEOUT_SECONDS=20
```

### 5) Run app
```bash
streamlit run app.py
```

Default URL:
- `http://localhost:8501`

## Configuration (.env)

### Why two keys?
- `GROQ_API_KEY`:
  - Used for question generation, evaluation, and follow-up logic.
- `TRANSLATION_GROQ_API_KEY`:
  - Used for translation only.

This enables operational separation and easier tuning.

### Recommended defaults
- Keep interview model lightweight for speed.
- Keep translation model high-quality for multilingual accuracy.

## Usage Guide

### Interviewer/Candidate flow
1. Open app.
2. Choose one of 10 interview languages.
3. Complete profile prompts.
4. Answer technical questions and follow-ups.
5. Receive final completion summary and score.

### Exit flow
At any time candidate can type:
- `exit`
- `quit`
- `bye`

The app saves available candidate data before ending.

### Restart flow
Use sidebar restart button to clear session and start a fresh interview.

## Technical Details

### Libraries used
- `streamlit`: interactive web UI.
- `requests`: Groq HTTP API calls.
- `python-dotenv`: environment variable loading.
- `googletrans`: fallback translation utility path.

### Core design decisions
- Canonical English processing:
  - All decision logic and prompts run in English.
- Output-only translation:
  - Translate final assistant text once per message.
- Translation caching:
  - Caches repeated translations to reduce latency.
- Strict evaluation schema:
  - Predictable score extraction and final score computation.

### State machine stages
- `greeting`
- `ask_name`
- `ask_email`
- `ask_phone`
- `ask_experience`
- `ask_position`
- `ask_location`
- `ask_tech_stack`
- `ask_question`
- `followup`
- `end`

## Prompt Design

### 1) Information gathering prompt strategy
Profile collection is deterministic (state machine), not open-ended. This avoids model variance in required fields and validation sequence.

### 2) Technical question generation prompt strategy
Prompt in `prompt_engine.py` enforces:
- Exactly 4 questions.
- Increasing difficulty.
- Scenario-based framing.
- No definition-style questions.
- English-only output.

Difficulty progression:
- Easy
- Medium
- Medium-hard
- Hard

### 3) Evaluation prompt strategy
Prompt in `evaluator.py` enforces:
- Strict rubric (Score 1-10).
- Relevance category.
- Short feedback.
- High-score constraints for depth/trade-offs.
- English-only output.

### 4) Follow-up prompt strategy
Prompt in `followup_generator.py` enforces:
- Exactly one concise follow-up.
- Conversational tone.
- Focus on identified gap.
- English-only output.

## Challenges and Solutions

### Challenge 1: Multilingual flow became slow
Problem:
- Multiple translation calls for pieces of one response increased latency.

Solution:
- Switched to one-pass output translation per assistant message.
- Added translation cache.
- Cached UI copy per language in session state.

### Challenge 2: Mixed-language scoring inconsistency
Problem:
- Evaluation quality dropped when prompts/answers mixed languages.

Solution:
- Canonical English processing pipeline.
- Translate user input to English before scoring.
- Keep prompts and expected outputs English-only.

### Challenge 3: Model roles were not clearly separated
Problem:
- Same model path handled both reasoning and translation.

Solution:
- Split model usage:
  - LLaMA for interview logic.
  - GPT-OSS for translation.
- Added separate translation key and config path.

### Challenge 4: Data normalization across languages
Problem:
- Stored data became inconsistent when candidates used different languages.

Solution:
- Save original values plus normalized English fields (`*_en`).
- Maintain language field for traceability.

### Challenge 5: Robustness with API/network variability
Problem:
- External API or translation service can fail.

Solution:
- Fallback behavior in translator.
- Timeout settings for both interview and translation model calls.

## Data Storage Schema
Records are appended to `data/candidates.json`.

Typical fields:
- `name`
- `email`
- `phone`
- `experience`
- `position`
- `location`
- `tech_stack`
- `language`
- `position_en`
- `location_en`
- `tech_stack_en`
- `final_score`

## Performance Notes
- Non-English interviews are always slower than English due to translation overhead.
- Current code minimizes overhead with:
  - Translation caching.
  - Single-pass translation for outgoing assistant responses.
  - UI text caching by language.
- For speed-sensitive scenarios:
  - Use a smaller translation model.
  - Reduce response verbosity in prompts.
  - Keep timeout values reasonable.

## Troubleshooting

### App starts but no response from model
- Verify `.env` keys.
- Check network and Groq availability.
- Confirm model IDs are valid for your account.

### Translation not applied
- Confirm `TRANSLATION_GROQ_API_KEY` is set.
- Confirm language selected in sidebar before interview starts.

### Slow responses in non-English mode
- This is expected due to translation step.
- Try lower-latency translation model via `TRANSLATION_MODEL`.

### Invalid email/phone rejected
- Email and phone validation is strict by design.
- Phone expects 10-15 digits, optional leading `+`.

## Future Improvements
- Async parallelization for translation and UI updates.
- Per-language prompt compression for faster generation.
- Background job queue for high-throughput interview sessions.
- Optional database backend (PostgreSQL) instead of JSON file persistence.
- Admin analytics dashboard for score trends by stack and role.

---
If you use this project in production, rotate API keys regularly and avoid storing secrets directly in source files.
