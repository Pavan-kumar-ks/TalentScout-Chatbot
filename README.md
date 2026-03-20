# 🤖 TalentScout - AI-Powered Hiring Assistant Chatbot

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation Instructions](#installation-instructions)
- [Usage Guide](#usage-guide)
- [Technical Details](#technical-details)
- [Prompt Design](#prompt-design)
- [Challenges & Solutions](#challenges--solutions)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)

---

## Project Overview

**TalentScout** is an intelligent, conversational AI-powered hiring assistant designed to streamline the recruitment process. It conducts automated technical interviews with candidates by:

- Collecting candidate information (name, email, phone, experience, position, location, tech stack)
- Generating contextual technical interview questions based on candidate expertise
- Evaluating candidate responses with detailed scoring and feedback
- Generating follow-up questions to probe deeper into candidate knowledge
- Storing candidate data and assessment results for HR review

The chatbot provides a seamless, conversational experience using Streamlit for the UI and Groq's Llama 3.3 API for intelligent question generation and evaluation.

### Key Capabilities
✅ **Adaptive Question Generation** - Creates difficulty-scaled questions (Easy → Hard)  
✅ **Real-time Evaluation** - Scores answers with relevance assessment and feedback  
✅ **Follow-up Intelligence** - Asks contextual follow-ups to assess depth of knowledge  
✅ **Data Persistence** - Saves candidate profiles and interview results  
✅ **Input Validation** - Validates email and phone formats before proceeding  
✅ **Sentiment Analysis** - Analyzes candidate confidence through response sentiment  

---

## Features

### 1. **Conversational Interview Flow**
- Guided, multi-stage interview process
- Natural language interactions
- State management to track interview progress

### 2. **Intelligent Question Generation**
- Context-aware questions based on tech stack and experience
- Four difficulty levels: Easy → Medium → Medium-Hard → Hard
- Scenario-based, practical questions (no definitions)

### 3. **Comprehensive Evaluation**
- Scoring system (1-10 scale with strict rubrics)
- Relevance assessment (Relevant, Weakly Relevant, Irrelevant)
- Detailed feedback highlighting gaps and areas for improvement

### 4. **Candidate Data Management**
- Stores all candidate information in JSON format
- Tracks interview responses and evaluations
- Enables easy review and candidate comparison

---

## Installation Instructions

### Prerequisites
- **Python 3.8+** installed on your system
- **Groq API Key** (sign up at [console.groq.com](https://console.groq.com))
- **Git** (for cloning the repository)
- **pip** (Python package manager)

### Step 1: Clone or Download the Repository
```bash
git clone <repository-url>
cd TalentScout-Chatbot
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:
- `streamlit==1.28.1` - Web UI framework
- `requests==2.31.0` - HTTP client for API calls
- `python-dotenv==1.0.0` - Environment variable management

### Step 4: Set Up Environment Variables
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_actual_groq_api_key_here
```

**Important:** Never commit the `.env` file to version control. Add it to `.gitignore`.

### Step 5: Run the Application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## Usage Guide

### Starting the Interview
1. Launch the application: `streamlit run app.py`
2. The chatbot greets you with a welcome message
3. Follow the conversational prompts to provide:
   - Full Name
   - Email Address
   - Phone Number
   - Years of Experience
   - Position(s) Applying For
   - Current Location
   - Tech Stack (languages, frameworks, tools)

### During the Interview
1. **Question Generation**: After providing your tech stack, the system generates 4 technical questions
2. **Answer Submission**: Respond to each question in the chat
3. **Evaluation**: Receive immediate scoring and feedback on your answer
4. **Follow-ups**: Answer contextual follow-up questions to demonstrate deeper knowledge

### Data Storage
- All candidate information is automatically saved to `data/candidates.json`
- Interview responses and scores are stored for later review

### Exiting the Interview
Type any of the following to end the conversation:
- `exit`
- `quit`
- `bye`

---

## Technical Details

### Architecture Overview
```
TalentScout-Chatbot/
├── app.py                          # Streamlit UI entry point
├── config.py                       # Configuration & environment variables
├── requirements.txt                # Project dependencies
├── data/
│   └── candidates.json            # Persistent candidate data storage
├── chatbot/
│   ├── llm_handler.py             # Groq API integration
│   ├── prompt_engine.py           # Prompt templates for question generation
│   ├── question_generator.py      # Question generation logic
│   ├── evaluator.py               # Answer evaluation with scoring
│   ├── followup_generator.py      # Follow-up question generation
│   ├── state_manager.py           # Interview state management
│   └── __init__.py
└── utils/
    ├── data_handler.py            # Candidate data persistence
    ├── sentiment.py               # Sentiment analysis of responses
    ├── validators.py              # Email & phone validation
    ├── helpers.py                 # Utility functions
    └── __init__.py
```

### Technologies & Libraries

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **UI Framework** | Streamlit 1.28.1 | Interactive web interface for the chatbot |
| **LLM Integration** | Groq API (Llama 3.3-70B) | Question generation, evaluation, and follow-ups |
| **HTTP Requests** | Requests 2.31.0 | API communication with Groq servers |
| **Environment** | python-dotenv 1.0.0 | Secure API key management |
| **Data Storage** | JSON | Lightweight candidate data persistence |
| **Validation** | Regex (Python built-in) | Email and phone number validation |

### Model Details

**LLM Model**: Groq - `llama-3.3-70b-versatile`
- **Why Llama 3.3?** 
  - Fast inference (sub-second responses)
  - Strong understanding of technical topics
  - Cost-effective compared to GPT-4
  - Excellent performance on reasoning tasks

**API Configuration**:
- Base URL: `https://api.groq.com/openai/v1/chat/completions`
- Temperature: 0.7 (balanced between creativity and consistency)
- Request Format: OpenAI-compatible API

### Key Modules

#### `llm_handler.py`
Handles all LLM API communication with error handling:
```python
- call_llm(prompt) → Sends prompt to Groq and returns response
- Supports streaming and error recovery
- Validates JSON responses
```

#### `prompt_engine.py`
Generates specialized prompts for different tasks:
```python
- build_question_prompt(tech_stack, experience) 
  → Creates prompt for question generation
```

#### `evaluator.py`
Evaluates candidate answers with strict rubrics:
```python
- evaluate_answer(question, answer)
  → Returns score (1-10), relevance, and feedback
```

#### `state_manager.py`
Manages interview conversation flow:
```python
- initialize_state() → Sets up initial interview state
- get_next_step(state, user_input) → Progresses through interview stages
```

---

## Prompt Design

### Philosophy
Prompts were carefully engineered to:
1. **Elicit Quality Responses** - Ask practical, scenario-based questions
2. **Maintain Consistency** - Ensure reproducible evaluation standards
3. **Minimize Hallucinations** - Provide strict output formats and rules
4. **Scale Difficulty** - Adapt question depth to candidate experience level

### Question Generation Prompt Strategy

**Objective**: Generate 4 technical questions with increasing difficulty

**Key Elements**:
- **Context Input**: Tech stack and years of experience
- **Difficulty Levels**: Explicitly defined (Easy → Hard)
- **Anti-Patterns**: Explicitly prohibit "What is X?" definition questions
- **Output Format**: Strict numbered format for easy parsing

**Example Structure**:
```
1. EASY: Practical understanding, real-world scenario
2. MEDIUM: Application-based, requires reasoning
3. MEDIUM-HARD: Optimization, trade-offs, performance
4. HARD: System design, edge cases, scalability
```

**Rules Enforced**:
- ❌ No definition questions
- ✅ All scenario-based inquiries
- ✅ Clear, concise questions
- ✅ Increasing complexity

### Evaluation Prompt Strategy

**Objective**: Score answers fairly with consistent rubric

**Scoring System**:
- **1-2**: Completely wrong / irrelevant
- **3-4**: Very weak, lacks understanding
- **5-6**: Basic idea, missing depth
- **7-8**: Good but incomplete, lacks edge cases
- **9-10**: Excellent, covers trade-offs and real-world usage

**Strictness Rules**:
- Scores 8+ require real-world reasoning OR trade-offs/optimization
- Generic answers max out at 6
- Shallow answers max out at 5

**Output Validation**: Structured format ensures parseable results
```
Score: X/10
Relevance: [Relevant | Weakly Relevant | Irrelevant]
Feedback: [2-3 lines of actionable feedback]
```

### Follow-up Generation Prompt

**Objective**: Ask natural, conversational follow-ups

**Constraints**:
- Max 1-2 lines (keep natural)
- Focus on knowledge gaps
- No labels or formal framing
- Conversational tone

---

## Challenges & Solutions

### Challenge 1: Question Parsing Inconsistency
**Problem**: LLM responses weren't always in the expected numbered format, breaking regex parsing

**Solution**:
- Implemented robust regex splitting on numbered patterns: `r"\n\d+\.\s"`
- Added fallback logic to return full response if parsing fails
- Clean up whitespace and empty entries post-parsing

```python
questions = re.split(r"\n\d+\.\s", response)
questions = [q.strip() for q in questions if q.strip()]
```

### Challenge 2: LLM Response Validation
**Problem**: API calls could fail silently or return incomplete data

**Solution**:
- Added explicit error checking for expected JSON structure
- Validate presence of required fields (`choices`, `message`)
- Return meaningful error messages to user

```python
if "choices" not in response_json:
    return f"LLM Error: {response_json}"
```

### Challenge 3: Scoring Consistency
**Problem**: LLM would rate answers generously without following strict rubrics

**Solution**:
- Implemented explicit, repetitive rubrics in prompts
- Added "IMPORTANT RULES" section with scoring caps
- Mentioned specific criteria for high scores (8+)
- Emphasized strictness at multiple points in prompt

### Challenge 4: State Management Complexity
**Problem**: Tracking multi-stage interview flow was prone to errors

**Solution**:
- Centralized state management in `state_manager.py`
- Clear stage definitions: greeting → name → email → phone → experience → position → location → tech_stack → questions
- Easy stage transitions with validation at each step

### Challenge 5: Data Persistence
**Problem**: Need to store candidate data reliably without a database

**Solution**:
- Used JSON format for simplicity and portability
- Implemented safe file handling with try-catch blocks
- Auto-create `data/candidates.json` if it doesn't exist
- Append new candidates to maintain history

### Challenge 6: Input Validation
**Problem**: Invalid emails and phone numbers were accepted

**Solution**:
- Created regex validators in `utils/validators.py`
- Email pattern: `r'^[\w\.-]+@[\w\.-]+\.\w+$'`
- Phone pattern: `r'^\+?\d{10,15}$'`
- Provide specific error messages for failed validation

### Challenge 7: Temperature-Based Response Variability
**Problem**: Interview experience was too random with high temperature

**Solution**:
- Set temperature to 0.7 (balanced approach)
- Provides consistent evaluation criteria
- Still allows for natural language generation
- Avoids overly deterministic or too random responses

---

## Project Structure

```
TalentScout-Chatbot/
│
├── 📄 app.py                    # Main Streamlit application
├── 📄 config.py                 # Configuration & environment setup
├── 📄 requirements.txt          # Python dependencies
├── 📄 README.md                 # This file
│
├── 📁 chatbot/                  # Core chatbot logic
│   ├── __init__.py
│   ├── llm_handler.py          # Groq API wrapper
│   ├── prompt_engine.py        # Prompt templates
│   ├── question_generator.py   # Question generation logic
│   ├── evaluator.py            # Answer evaluation
│   ├── followup_generator.py   # Follow-up questions
│   └── state_manager.py        # Interview state machine
│
├── 📁 utils/                    # Utility modules
│   ├── __init__.py
│   ├── data_handler.py         # Candidate data storage
│   ├── sentiment.py            # Sentiment analysis
│   ├── validators.py           # Input validation
│   └── helpers.py              # Helper functions
│
├── 📁 data/                     # Data storage
│   └── candidates.json         # Candidate interview records
│
└── 📁 __pycache__/            # Python cache (ignore)
```

---

## Future Enhancements

### Phase 2 Features
- [ ] **Database Integration** - Replace JSON with PostgreSQL/MongoDB for scalability
- [ ] **Video Interview** - Add video recording capability for reference
- [ ] **Skill Assessment Matrix** - Generate candidate skill reports
- [ ] **Interview Analytics** - Track hiring funnel, time-to-hire, average scores
- [ ] **Multi-language Support** - Conduct interviews in Hindi, Spanish, Mandarin, etc.
- [ ] **Resume Parsing** - Auto-populate candidate info from resume upload

### Phase 3 Enhancements
- [ ] **Behavioral Questions** - Add soft skills assessment
- [ ] **Coding Challenges** - Integrate live code execution (LeetCode-style)
- [ ] **Candidate Portal** - Self-service interview scheduling and tracking
- [ ] **Admin Dashboard** - Real-time hiring manager interface
- [ ] **AI-Powered Recommendations** - Suggest pass/fail decisions

### Performance Optimizations
- [ ] Implement response caching for similar questions
- [ ] Add Groq API rate limiting and retry logic
- [ ] Optimize JSON operations for large candidate datasets
- [ ] Add background job processing for evaluations

---

## Troubleshooting

### Issue: `GROQ_API_KEY not found`
**Solution**: Ensure `.env` file exists in project root with valid API key
```bash
echo GROQ_API_KEY=your_key > .env
```

### Issue: Streamlit not loading
**Solution**: Verify installation and clear cache
```bash
pip install --upgrade streamlit
streamlit run app.py --client.disableFileWatcher false
```

### Issue: API Rate Limiting
**Solution**: Groq has rate limits. If you hit them:
- Wait a few minutes before retrying
- Consider caching frequently asked questions
- Contact Groq support for rate limit increase

### Issue: JSON Parse Errors
**Solution**: Validate `data/candidates.json` format. If corrupted:
```bash
# Backup and reset
mv data/candidates.json data/candidates.json.bak
echo "[]" > data/candidates.json
```

---

## Contributing

We welcome contributions! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Support & Contact

For issues, questions, or suggestions:
- 📧 Email: support@talentscout.ai
- 🐛 Report Bugs: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

## Acknowledgments

- **Groq** - Fast LLM inference platform
- **Streamlit** - Rapid web app development
- **Llama 3.3** - Open-source language model

---

**Last Updated**: March 21, 2026  
**Version**: 1.0.0
