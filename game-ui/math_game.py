from itertools import product
import random

class MathGame():
    list_of_operators = ['+', '-', '*']
    
    def __init__(self, choose_game: int, left_nbr: int, right_nbr: int):
        self.choose_game = choose_game
        self.left_nbr = left_nbr
        self.right_nbr = right_nbr
        self.score = 0
        self.question_answers = []
        
        
    def setup_questions(self):
        operator = self.list_of_operators[self.choose_game]
        combos = list( product( [x for x in range(1, self.left_nbr + 1)], [y for y in range(1, self.right_nbr + 1)])) 
        unique_combos = set((min(x, y), max(x, y)) for x, y in combos)
        for i, (left, right) in enumerate(unique_combos):
            question = f"{left}{operator}{right}"
            self.question_answers.append((question,eval(question)))
    
    def play_game(self):
        self.setup_questions()
        random.shuffle(self.question_answers)
        for question, answer in self.question_answers:
            print(f"What is the answer to {question}?")
            user_answer = input()
            if int(user_answer) == answer:
                self.score += 1
            
        print(f"Your score is {self.score}")