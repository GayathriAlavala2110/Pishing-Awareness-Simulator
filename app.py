from flask import Flask, render_template, request, session, redirect, url_for
import json
import random

app = Flask(__name__)

app.secret_key = "phishing-awareness-secret"

# Load questions
with open("questions.json", "r", encoding="utf-8") as file:
    questions = json.load(file)


@app.route("/")
def home():
    return render_template("learning.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    # Start a new quiz attempt
    if "used_questions" not in session:
        session["used_questions"] = []
        session["question_count"] = 0
        session["score"] = 0

    # -------------------------
    # SUBMIT ANSWER
    # -------------------------
    if request.method == "POST":

        current_index = session["current_question"]
        question = questions[current_index]

        selected_answer = request.form.get("answer")
        user_reason = request.form.get("user_reason")

        correct = selected_answer == question["answer"]
        if "score" not in session:
            session["score"] = 0

        if correct:
           session["score"] += 1

        return render_template(
            "quiz.html",
            question=question,
            feedback=True,
            selected_answer=selected_answer,
            user_reason=user_reason,
            correct=correct,
            quiz_complete=False
        )

    # -------------------------
    # NEXT QUESTION
    # -------------------------

    # Complete quiz after 8 questions
    if session["question_count"] >= 8:
        score=session.get("score",0)

        session.pop("used_questions", None)
        session.pop("question_count", None)
        session.pop("current_question", None)

        return render_template(
            "quiz.html",
            quiz_complete=True,
            score=score,
            total=8
        )

    # Find unused questions
    available_questions = [
        i for i in range(len(questions))
        if i not in session["used_questions"]
    ]

    # Random question
    current_index = random.choice(available_questions)

    session["current_question"] = current_index

    # Remember question
    used = session["used_questions"]
    used.append(current_index)
    session["used_questions"] = used

    # Increase question count
    session["question_count"] += 1

    question = questions[current_index]

    return render_template(
        "quiz.html",
        question=question,
        feedback=False,
        quiz_complete=False
    )


if __name__ == "__main__":
    app.run(debug=True)