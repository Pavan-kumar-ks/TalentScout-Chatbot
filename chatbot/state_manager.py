# from utils.validators import is_valid_email, is_valid_phone
# from chatbot.question_generator import generate_questions
# from chatbot.evaluator import evaluate_answer
# from chatbot.followup_generator import generate_followup
# from chatbot.llm_handler import call_llm
# from utils.helpers import is_weak_answer
# from utils.sentiment import analyze_sentiment
# from utils.data_handler import save_candidate


# def initialize_state():
#     return {
#         "stage": "greeting",
#         "candidate": {
#             "name": "",
#             "email": "",
#             "phone": "",
#             "experience": "",
#             "position": "",
#             "location": "",
#             "tech_stack": ""
#         },
#         "questions": [],
#         "current_question_index": 0,
#         "evaluations": []
#     }


# def extract_score(evaluation):
#     try:
#         return int(evaluation.split("Score:")[1].split("/")[0].strip())
#     except:
#         return 0


# def calculate_final_score(evaluations):
#     scores = [extract_score(e) for e in evaluations if "Score:" in e]
#     return sum(scores) // len(scores) if scores else 0


# def save_final_candidate(state):
#     candidate = state["candidate"]
#     final_score = calculate_final_score(state["evaluations"])

#     candidate_data = {
#         "name": candidate["name"],
#         "email": candidate["email"],
#         "phone": candidate["phone"],
#         "experience": candidate["experience"],
#         "position": candidate["position"],
#         "location": candidate["location"],
#         "tech_stack": candidate["tech_stack"],
#         "final_score": final_score
#     }

#     save_candidate(candidate_data)


# def get_next_step(state, user_input):
#     stage = state["stage"]
#     candidate = state["candidate"]
#     user_input = user_input.strip()

#     # EXIT
#     if user_input.lower() in ["exit", "quit", "bye"]:
#         save_final_candidate(state)
#         state["stage"] = "end"
#         return f"""
# 👋 Interview ended.

# Thank you, {candidate.get("name", "Candidate")}!

# If you wish to continue later, feel free to restart.

# Have a great day 🚀
# """

#     # =========================
#     # GREETING
#     # =========================
#     if stage == "greeting":
#         state["stage"] = "ask_name"
#         return "👋 Welcome to TalentScout!\n\nWhat is your full name?"

#     # =========================
#     # INFO COLLECTION
#     # =========================

#     elif stage == "ask_name":
#         candidate["name"] = user_input
#         state["stage"] = "ask_email"
#         return "📧 Enter your email:"

#     elif stage == "ask_email":
#         if not is_valid_email(user_input):
#             return "❌ Invalid email format."
#         candidate["email"] = user_input
#         state["stage"] = "ask_phone"
#         return "📱 Enter your phone number:"

#     elif stage == "ask_phone":
#         if not is_valid_phone(user_input):
#             return "❌ Invalid phone number."
#         candidate["phone"] = user_input
#         state["stage"] = "ask_experience"
#         return "💼 Years of experience?"

#     elif stage == "ask_experience":
#         if not user_input.isdigit():
#             return "❌ Enter a valid number."
#         candidate["experience"] = user_input
#         state["stage"] = "ask_position"
#         return "🎯 Desired role?"

#     elif stage == "ask_position":
#         candidate["position"] = user_input
#         state["stage"] = "ask_location"
#         return "📍 Current location?"

#     elif stage == "ask_location":
#         candidate["location"] = user_input
#         state["stage"] = "ask_tech_stack"
#         return "🧠 Enter your tech stack:"

#     # =========================
#     # QUESTION GENERATION
#     # =========================

#     elif stage == "ask_tech_stack":
#         candidate["tech_stack"] = user_input

#         questions = generate_questions(
#             candidate["tech_stack"],
#             candidate["experience"]
#         )

#         state["questions"] = questions
#         state["current_question_index"] = 0
#         state["stage"] = "ask_question"

#         return f"🚀 Technical Round Begins\n\nQuestion 1:\n{questions[0]}"

#     # =========================
#     # MAIN QUESTION FLOW
#     # =========================

#     elif stage == "ask_question":
#         idx = state["current_question_index"]
#         current_question = state["questions"][idx]

#         sentiment = analyze_sentiment(user_input)

#         if is_weak_answer(user_input):
#             explanation = call_llm(f"Explain simply:\n{current_question}")

#             idx += 1
#             if idx >= len(state["questions"]):
#                 save_final_candidate(state)
#                 state["stage"] = "end"
#                 return f"""
# 📘 Explanation:
# {explanation}

# 🎉 Interview Completed!

# 🙏 Thank you, {candidate['name']}.

# Our team will review your responses and contact you within 2–5 business days.
# """

#             state["current_question_index"] = idx
#             return f"📘 Explanation:\n{explanation}\n\n➡️ Question {idx+1}:\n{state['questions'][idx]}"

#         evaluation = evaluate_answer(current_question, user_input)
#         state["evaluations"].append(evaluation)

#         score = extract_score(evaluation)

#         if score >= 7:
#             tone = "✅ Strong answer\n"
#         elif score >= 4:
#             tone = "👍 Decent attempt\n"
#         else:
#             tone = "⚠️ Needs improvement\n"

#         if "Irrelevant" in evaluation:
#             followup = "Your answer seems unrelated. Try focusing on the problem."
#         else:
#             followup = generate_followup(current_question, user_input)

#         state["stage"] = "followup"

#         return f"{tone}\n🧠 {evaluation}\n\n🔎 {followup}"

#     # =========================
#     # FOLLOW-UP FLOW
#     # =========================

#     elif stage == "followup":
#         idx = state["current_question_index"]
#         current_question = state["questions"][idx]

#         evaluation = evaluate_answer(current_question, user_input)

#         idx += 1

#         if idx >= len(state["questions"]):
#             save_final_candidate(state)
#             state["stage"] = "end"
#             return f"""
# 🧠 Follow-up Evaluation:
# {evaluation}

# 🎉 Interview Completed!

# 📊 Final Score: {calculate_final_score(state["evaluations"])}/10

# 🙏 Thank you, {candidate["name"]}, for participating.

# 📌 Next Steps:
# - Your responses will be reviewed by our team
# - If shortlisted, you will be contacted for further rounds

# ⏳ Expect an update within 2–5 business days.

# Best of luck 🚀
# """

#         state["current_question_index"] = idx
#         state["stage"] = "ask_question"

#         return f"🧠 Follow-up Evaluation:\n{evaluation}\n\n➡️ Question {idx+1}:\n{state['questions'][idx]}"

#     elif stage == "end":
#         return "Conversation has ended."

#     return "I didn't understand that. Please try again."












from utils.validators import is_valid_email, is_valid_phone
from chatbot.question_generator import generate_questions
from chatbot.evaluator import evaluate_answer
from chatbot.followup_generator import generate_followup
from chatbot.llm_handler import call_llm
from utils.helpers import is_weak_answer
from utils.sentiment import analyze_sentiment
from utils.data_handler import save_candidate
from utils.translator import translate_to_english


def initialize_state():
    return {
        "stage": "greeting",
        "candidate": {
            "name": "",
            "email": "",
            "phone": "",
            "experience": "",
            "position": "",
            "location": "",
            "tech_stack": ""
        },
        "questions": [],
        "current_question_index": 0,
        "evaluations": []
    }


def extract_score(evaluation):
    try:
        return int(evaluation.split("Score:")[1].split("/")[0].strip())
    except:
        return 0


def calculate_final_score(evaluations):
    scores = [extract_score(e) for e in evaluations if "Score:" in e]
    return sum(scores) // len(scores) if scores else 0


def save_final_candidate(state):
    candidate = state["candidate"]

    candidate_data = {
        "name": candidate["name"],
        "email": candidate["email"],
        "phone": candidate["phone"],
        "experience": candidate["experience"],
        "position": candidate["position"],
        "location": candidate["location"],
        "tech_stack": candidate["tech_stack"],
        "final_score": calculate_final_score(state["evaluations"])
    }

    save_candidate(candidate_data)


def get_next_step(state, user_input):
    stage = state["stage"]
    candidate = state["candidate"]

    # 🌍 Translate input
    user_input = translate_to_english(user_input.strip())

    # EXIT
    if user_input.lower() in ["exit", "quit", "bye"]:
        save_final_candidate(state)
        state["stage"] = "end"
        return "👋 Interview ended. Thank you!"

    # =========================
    # GREETING
    # =========================
    if stage == "greeting":
        state["stage"] = "ask_name"
        return "👋 Welcome to TalentScout!\n\nWhat is your full name?"

    # =========================
    # INFO COLLECTION
    # =========================

    elif stage == "ask_name":
        candidate["name"] = user_input
        state["stage"] = "ask_email"
        return f"Nice to meet you {candidate['name']}! 📧 Enter your email:"

    elif stage == "ask_email":
        if not is_valid_email(user_input):
            return "❌ Invalid email."
        candidate["email"] = user_input
        state["stage"] = "ask_phone"
        return "📱 Phone number?"

    elif stage == "ask_phone":
        if not is_valid_phone(user_input):
            return "❌ Invalid phone."
        candidate["phone"] = user_input
        state["stage"] = "ask_experience"
        return "💼 Years of experience?"

    elif stage == "ask_experience":
        if not user_input.isdigit():
            return "❌ Enter valid number."
        candidate["experience"] = user_input
        state["stage"] = "ask_position"
        return "🎯 Desired role?"

    elif stage == "ask_position":
        candidate["position"] = user_input
        state["stage"] = "ask_location"
        return "📍 Location?"

    elif stage == "ask_location":
        candidate["location"] = user_input
        state["stage"] = "ask_tech_stack"
        return "🧠 Tech stack?"

    # =========================
    # QUESTIONS
    # =========================

    elif stage == "ask_tech_stack":
        candidate["tech_stack"] = user_input

        questions = generate_questions(
            candidate["tech_stack"],
            candidate["experience"]
        )

        state["questions"] = questions
        state["current_question_index"] = 0
        state["stage"] = "ask_question"

        return f"🚀 Technical Round Begins\n\nQuestion 1:\n{questions[0]}"

    elif stage == "ask_question":
        idx = state["current_question_index"]
        current_question = state["questions"][idx]

        sentiment = analyze_sentiment(user_input)

        # Weak answer
        if is_weak_answer(user_input):
            explanation = call_llm(f"Explain simply:\n{current_question}")

            idx += 1
            if idx >= len(state["questions"]):
                save_final_candidate(state)
                state["stage"] = "end"
                return f"📘 {explanation}\n\n🎉 Interview Completed!"

            state["current_question_index"] = idx
            return f"📘 {explanation}\n\n➡️ Question {idx+1}:\n{state['questions'][idx]}"

        # Evaluate
        evaluation = evaluate_answer(current_question, user_input)
        state["evaluations"].append(evaluation)

        score = extract_score(evaluation)

        if score >= 7:
            tone = "✅ Strong answer\n"
        elif score >= 4:
            tone = "👍 Decent attempt\n"
        else:
            tone = "⚠️ Needs improvement\n"

        # Sentiment tone
        if sentiment == "negative":
            tone += "No worries, keep going 👍\n"

        if "Irrelevant" in evaluation:
            followup = "Please focus on the question."
        else:
            followup = generate_followup(current_question, user_input)

        state["stage"] = "followup"

        return f"{tone}\n🧠 {evaluation}\n\n🔎 {followup}"

    elif stage == "followup":
        idx = state["current_question_index"]
        current_question = state["questions"][idx]

        evaluation = evaluate_answer(current_question, user_input)

        idx += 1

        if idx >= len(state["questions"]):
            save_final_candidate(state)
            state["stage"] = "end"
            return f"🧠 {evaluation}\n\n🎉 Interview Completed!"

        state["current_question_index"] = idx
        state["stage"] = "ask_question"

        return f"🧠 {evaluation}\n\n➡️ Question {idx+1}:\n{state['questions'][idx]}"

    return "I didn't understand. Try again."