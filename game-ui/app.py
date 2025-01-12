import time
from flask import Flask, render_template, request, redirect, url_for
from math_game import MathGame

app = Flask(__name__)

game_instance = None  # Store the game instance
start_time = None  # Record when the game starts

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_game():
    global game_instance, start_time
    # Initialize the game instance (existing logic)
    choose_game = int(request.form["choose_game"])
    left_nbr = int(request.form["left_nbr"])
    right_nbr = int(request.form["right_nbr"])
    start_time = time.time()  # Record the start time
    game_instance = MathGame(choose_game, left_nbr, right_nbr)
    game_instance.setup_questions()
    return redirect(url_for("play_game"))

@app.route("/play", methods=["GET", "POST"])
def play_game():
    global game_instance, start_time
    if not game_instance:
        return redirect(url_for("index"))

    # Handle the gameplay logic
    if request.method == "POST":
        user_answer = int(request.form["answer"])
        question_idx = int(request.form["question_idx"])
        question, correct_answer = game_instance.question_answers[question_idx]
        if user_answer == correct_answer:
            game_instance.score += 1

        if question_idx + 1 < len(game_instance.question_answers):
            return redirect(url_for("play_game", question_idx=question_idx + 1))
        else:
            return redirect(url_for("game_over"))

    # Pass the elapsed time to the frontend
    elapsed_time = round(time.time() - start_time, 2)
    question_idx = int(request.args.get("question_idx", 0))
    question, _ = game_instance.question_answers[question_idx]
    return render_template("play.html", question=question, question_idx=question_idx, score=game_instance.score, elapsed_time=elapsed_time)

@app.route("/game_over")
def game_over():
    global game_instance, start_time
    elapsed_time = round(time.time() - start_time, 2)
    return render_template("game_over.html", score=game_instance.score, time_elapsed=elapsed_time)

if __name__ == "__main__":
    app.run(debug=True)
