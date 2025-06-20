import json
import time

class QuizApp: #base class
    def __init__(self, users, score, questions, time_taken):
        self.users = users
        self.score = score
        self.questions = questions
        self.time_taken = time_taken
        self.current_user = None

    def saveuserprogress(self): # function to save user progress
        with open("usersprogress.json", "w") as save:
            json.dump({
                "users": self.users,
                "score": self.score,
                "time_taken": self.time_taken
            }, save, indent=3) # indentaion for better understanding of the data

    def ask_question(self, question): # function for asking questions
        if self.current_user is None:
            print(question)