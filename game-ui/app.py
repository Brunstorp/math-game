from flask import Flask, render_template, request, redirect, url_for, jsonify
from math_game import MathGame
import random

app = Flask(__name__)

# Store game instance globally (temporary; improve later with sessions)
game_instance = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_game():
    global game_instance
    # Get and validate form inputs
    try:
        choose_game = int(request.form["choose_game"])
        left_nbr = int(request.form["left_nbr"])
        right_nbr = int(request.form["right_nbr"])
        
        if left_nbr < 1 or right_nbr < 1:
            return "Error: Numbers must be greater than 0", 400
    except (ValueError, KeyError):
        return "Invalid input. Please go back and try again.", 400
    
    # Initialize the game
    game_instance = MathGame(choose_game, left_nbr, right_nbr)
    game_instance.setup_questions()
    random.shuffle(game_instance.question_answers)
    
    # Redirect to the play page
    return redirect(url_for("play_game"))

@app.route("/play", methods=["GET", "POST"])
def play_game():
    global game_instance
    if not game_instance:
        return redirect(url_for("index"))
    
    if request.method == "POST":
        # Process the user's answer
        user_answer = int(request.form["answer"])
        question_idx = int(request.form["question_idx"])
        question, correct_answer = game_instance.question_answers[question_idx]
        
        # Check the answer and update the score
        if user_answer == correct_answer:
            game_instance.score += 1
        
        # Move to the next question or end the game
        if question_idx + 1 < len(game_instance.question_answers):
            next_question = question_idx + 1
            return redirect(url_for("play_game", question_idx=next_question))
        else:
            return redirect(url_for("game_over"))
    
    # Display the current question
    question_idx = int(request.args.get("question_idx", 0))
    question, _ = game_instance.question_answers[question_idx]
    return render_template("play.html", question=question, question_idx=question_idx, score=game_instance.score)

@app.route("/game_over")
def game_over():
    global game_instance
    return render_template("game_over.html", score=game_instance.score)

if __name__ == "__main__":
    app.run(debug=True)
