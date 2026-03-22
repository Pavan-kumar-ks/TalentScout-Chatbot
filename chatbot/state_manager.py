from utils.validators import is_valid_email, is_valid_phone
from chatbot.question_generator import generate_questions
from chatbot.evaluator import evaluate_answer
from chatbot.followup_generator import generate_followup
from chatbot.llm_handler import call_llm
from utils.helpers import is_weak_answer
from utils.sentiment import analyze_sentiment
from utils.data_handler import save_candidate
from utils.translator import normalize_language, translate_to_english, translate_to_language


def initialize_state():
    return {
        "stage": "greeting",
        "language": "en",
        "candidate": {
            "name": "",
            "email": "",
            "phone": "",
            "experience": "",
            "position": "",
            "location": "",
            "tech_stack": "",
        },
        "questions": [],
        "current_question_index": 0,
        "evaluations": [],
    }


def extract_score(evaluation):
    try:
        return int(evaluation.split("Score:")[1].split("/")[0].strip())
    except Exception:
        return 0


def calculate_final_score(evaluations):
    scores = [extract_score(e) for e in evaluations if "Score:" in e]
    return sum(scores) // len(scores) if scores else 0


def get_language(state):
    return normalize_language(state.get("language", "en"))


def to_english_for_processing(state, text):
    language = get_language(state)
    text = (text or "").strip()
    if not text:
        return ""
    if language == "en":
        return text
    return translate_to_english(text, src_lang=language)


def to_user_language(state, english_text):
    language = get_language(state)
    if language == "en":
        return english_text
    return translate_to_language(english_text, language=language, src_lang="en")


def save_final_candidate(state):
    candidate = state["candidate"]
    language = get_language(state)

    candidate_data = {
        "name": candidate["name"],
        "email": candidate["email"],
        "phone": candidate["phone"],
        "experience": candidate["experience"],
        "position": candidate["position"],
        "location": candidate["location"],
        "tech_stack": candidate["tech_stack"],
        "language": language,
        "position_en": translate_to_english(candidate["position"], src_lang=language),
        "location_en": translate_to_english(candidate["location"], src_lang=language),
        "tech_stack_en": translate_to_english(candidate["tech_stack"], src_lang=language),
        "final_score": calculate_final_score(state["evaluations"]),
    }

    save_candidate(candidate_data)


def get_next_step(state, user_input):
    stage = state["stage"]
    candidate = state["candidate"]
    raw_input = (user_input or "").strip()
    processed_input = to_english_for_processing(state, raw_input)

    if processed_input.lower() in ["exit", "quit", "bye"]:
        save_final_candidate(state)
        state["stage"] = "end"
        return to_user_language(state, "Interview ended. Thank you!")

    if stage == "greeting":
        state["stage"] = "ask_name"
        return to_user_language(state, "Welcome to TalentScout!\n\nWhat is your full name?")

    if stage == "ask_name":
        candidate["name"] = raw_input
        state["stage"] = "ask_email"
        english_response = f"Nice to meet you {candidate['name']}! Enter your email:"
        return to_user_language(state, english_response)

    if stage == "ask_email":
        if not is_valid_email(raw_input):
            return to_user_language(state, "Invalid email format. Please enter a valid email.")
        candidate["email"] = raw_input
        state["stage"] = "ask_phone"
        return to_user_language(state, "Enter your phone number (10 to 15 digits, optional +):")

    if stage == "ask_phone":
        if not is_valid_phone(raw_input):
            return to_user_language(state, "Invalid phone number format. Please enter a valid number.")
        candidate["phone"] = raw_input
        state["stage"] = "ask_experience"
        return to_user_language(state, "How many years of experience do you have?")

    if stage == "ask_experience":
        if not processed_input.isdigit():
            return to_user_language(state, "Please enter experience as a number.")
        candidate["experience"] = processed_input
        state["stage"] = "ask_position"
        return to_user_language(state, "What role are you applying for?")

    if stage == "ask_position":
        candidate["position"] = raw_input
        state["stage"] = "ask_location"
        return to_user_language(state, "What is your current location?")

    if stage == "ask_location":
        candidate["location"] = raw_input
        state["stage"] = "ask_tech_stack"
        return to_user_language(state, "Enter your primary tech stack (comma separated):")

    if stage == "ask_tech_stack":
        candidate["tech_stack"] = raw_input

        tech_stack_en = translate_to_english(raw_input, src_lang=get_language(state))
        questions = generate_questions(tech_stack_en, candidate["experience"])

        state["questions"] = questions
        state["current_question_index"] = 0
        state["stage"] = "ask_question"

        english_response = f"Technical round begins.\n\nQuestion 1:\n{questions[0]}"
        return to_user_language(state, english_response)

    if stage == "ask_question":
        idx = state["current_question_index"]
        current_question = state["questions"][idx]

        sentiment = analyze_sentiment(processed_input)

        if is_weak_answer(processed_input):
            explanation = call_llm(
                f"Explain this interview question simply in English:\n\n{current_question}"
            )

            idx += 1
            if idx >= len(state["questions"]):
                save_final_candidate(state)
                state["stage"] = "end"
                english_response = f"Explanation:\n{explanation}\n\nInterview completed!"
                return to_user_language(state, english_response)

            state["current_question_index"] = idx
            english_response = (
                f"Explanation:\n{explanation}\n\n"
                f"Question {idx + 1}:\n{state['questions'][idx]}"
            )
            return to_user_language(state, english_response)

        evaluation = evaluate_answer(current_question, processed_input)
        state["evaluations"].append(evaluation)

        score = extract_score(evaluation)
        if score >= 7:
            tone = "Strong answer"
        elif score >= 4:
            tone = "Decent attempt"
        else:
            tone = "Needs improvement"

        if sentiment == "negative":
            tone += "\nNo worries, keep going."

        if "Irrelevant" in evaluation:
            followup = "Please focus on the question."
        else:
            followup = generate_followup(current_question, processed_input)

        state["stage"] = "followup"
        english_response = (
            f"{tone}\n\nEvaluation:\n{evaluation}\n\nFollow-up:\n{followup}"
        )
        return to_user_language(state, english_response)

    if stage == "followup":
        idx = state["current_question_index"]
        current_question = state["questions"][idx]

        evaluation = evaluate_answer(current_question, processed_input)
        state["evaluations"].append(evaluation)

        idx += 1

        if idx >= len(state["questions"]):
            save_final_candidate(state)
            state["stage"] = "end"
            final_score = calculate_final_score(state["evaluations"])
            english_response = (
                f"Follow-up evaluation:\n{evaluation}\n\n"
                f"Interview completed!\nFinal score: {final_score}/10"
            )
            return to_user_language(state, english_response)

        state["current_question_index"] = idx
        state["stage"] = "ask_question"

        english_response = (
            f"Follow-up evaluation:\n{evaluation}\n\n"
            f"Question {idx + 1}:\n{state['questions'][idx]}"
        )
        return to_user_language(state, english_response)

    if stage == "end":
        return to_user_language(state, "Conversation has ended.")

    return to_user_language(state, "I did not understand that. Please try again.")
