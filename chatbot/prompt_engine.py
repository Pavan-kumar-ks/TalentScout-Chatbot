def build_question_prompt(tech_stack, experience):
    return f"""
You are a senior software engineer conducting a technical interview.

Tech Stack: {tech_stack}
Candidate Experience: {experience} years

Generate EXACTLY 4 technical questions with INCREASING difficulty.

Difficulty Levels:

1. EASY:
- Basic practical understanding
- Real-world but simple
- No theory definitions

2. MEDIUM:
- Application-based
- Requires reasoning
- Slightly deeper than basics

3. MEDIUM-HARD:
- Optimization / performance / trade-offs
- Requires deeper thinking

4. HARD:
- System design OR edge cases OR scalability
- Tests deep expertise

STRICT RULES:
- Do NOT ask definitions
- Do NOT ask "What is X?"
- All questions must be scenario-based
- Keep each question clear and concise

Output format ONLY:

1. <easy question>
2. <medium question>
3. <medium-hard question>
4. <hard question>
"""