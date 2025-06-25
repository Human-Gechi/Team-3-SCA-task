import json
import time
import random
# base class for the quiz
class QuizApp:
    """
    A class that allows users to rake a quiz on open source questions"""
    def __init__(self): # initializing the quiz app
        self.users = []
        self.score = 0
        self.questions = []
        self.time_taken = 0
        self.current_user = None

    def load_questions(self, filepath): # function to laod questions from the json file
        try: # try except block to handle opening the file
            with open(filepath, "r") as file:
                data = json.load(file)
                self.questions = data['questions']
        except FileNotFoundError: # if the file is not found,the message below is printed
            print(f"Error: The file {filepath} does not exist.")

    def adduser(self, username): # function to add a new user
        if username not in self.users: # if the user is not in the list of users, add the user
            self.users.append(username) # append the username to the list of`users`
            self.current_user = username # seetting the current user to the username
            print(f"{username} has been added.") #output message as confirmation that the user has been added
        else:
            print(f"{username} already exists.") # if the user exixts,print the message below
            self.current_user = username
        self.saveuserprogress() # saving the user's progress after adding the user.

    def saveuserprogress(self):# function to save the user's progress
        try: #try except block to handle opening the file has holds user's progress
            with open("usersprogress.json", "r") as file: # reading the file
                data = json.load(file)
        except FileNotFoundError:
            data = []

        #To update or add current user's score
        available = False
        for user in data: # this updated loop checks if the user is already in the list of users in the file
            # if the user is already in the list of users, the score is updated and time taken
            if user["user"] == self.current_user:
                user["score"] = self.score
                user["time_taken"] = self.time_taken
                available = True
                break

        if not available:  # if the user is not in the list, add the user
            data.append({
                "user": self.current_user,
                "score": self.score,
                "time_taken": self.time_taken
            })

        with open("usersprogress.json", "w") as save: # writing the changes to the json file
            json.dump(data, save, indent=3) # wrting  the data in python dictionary format and it is converted to json format using json.dump

    def ask_question(self, question): # function to ask a question
        print(question['question'])
        answer = input("Enter your answer: ")
        return answer, question['answer']

    def exitquiz(self): # functio to exit quiz
        if self.current_user:
            print("Progress has been saved.")
            self.saveuserprogress()
            self.current_user = None
        else:
            print("No user is logged in.")
    def leaderboard(self): # function to display who is leading in the quiz
        print("\nLeaderboard:")
        try:
            with open("usersprogress.json", "r") as file: # reading the file holding user's progress
                data = json.load(file) # laoding data from the file
                if isinstance(data, list): #checking if the file is in a list using isinstance(object, datatype) function
                    sorted_users = sorted(data, key=lambda x: x["score"], reverse=True)# sorting each user's score in descending order
                    for i, user in enumerate(sorted_users, start=1): # ranking each user based o their scores
                        print(f"Rank {i}: {user['user']} - Score: {user['score']} - Time: {user['time_taken']:.2f}s") # format for dsplaying leaderboard
                else:
                    print("Invalid data format.") # error message
        except FileNotFoundError:
            print("No leaderboard data found.")

    def startquiz(self):# functio to start the quiz
        self.load_questions("opensource_questions.json")# loading the json question in the opensource_questions.json file
        if not self.questions: # checking if questions are available
            print("Questions are not available.")
            return
        username = input("Enter your username:")# user is prompted to enter their username
        self.adduser(username)

        print(f"Starting quiz for {self.current_user}") #message to confirm that the quiz has started for the user
        start_time = time.time() # counting the time started
        self.score = 0  # reset score before quiz
        random.shuffle(self.questions)#randomly shuffle opensource questions

        for question in self.questions:
            answer, correct = self.ask_question(question)
            if answer.upper() == correct.upper(): # checking if the answer is correct
                print("Correct!") # output message if correct
                self.score += 1 #1 is added to the score if the answer is correct
            else:
                print(f"Wrong. The correct answer was: {correct}") # if the answer is wrong, the correct answer is displayed
            continuation = input("Continue? (yes/no): ") # asking user if they wish to continue
            if continuation.lower() != "yes": # if the user does not wish to continue,that ends the quiz, the loop breaks
                break

        end_time = time.time() # time after answering questions
        self.time_taken = end_time - start_time # calculating the time taken to complete the quiz
        self.saveuserprogress() # saving users progress after the quiz is completed in the userprogress.json file
        print(f"Quiz complete! Score: {self.score}, Time: {self.time_taken:.2f}s")