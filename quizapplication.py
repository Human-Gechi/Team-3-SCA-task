#importing necessary libraries
import streamlit as st
import json
import os
#base class for quiz application
class QuizApp:
    def __init__(self):
        self.users = [] # list of userd
        self.score = 0 #setting initial score
        self.questions = [] # list of questions
        self.time_taken = 0 # initial time taken
        self.username = "" #username
        self.user_answers = [] # list of answers provided

    def adduser(self, username): # function to add user
        if username not in self.users: #appending users to the lsit of users
            self.users.append(username)

    def load_questions(self, filename): #loading questions fromthe json file
        try:
            with open(filename, 'r') as file: #reading the file using context mananger
                data = json.load(file) #
            if isinstance(data, dict) and "questions" in data: #format of the json file
                self.questions = data["questions"]
            else:
                self.questions = [] #return an empty list if question is not found
        except FileNotFoundError: # except filenotfounderror
            self.questions = [] #return an empty list
#Function to ask questions
    def ask_question(self, question, index):
        """"
        Function name: ask_questions
        param : {
                self - initialization from the base class
                question - argument for each question
                index - providing an index for each question
        }
        """
        st.write(f"Q{index + 1}: {question['question']}") # creating an index for each question starting from 1
        if f"user_answer_{index}" not in st.session_state:
            st.session_state[f"user_answer_{index}"] = None
        # answers functionality

        """Using st.radio to provide options for icking an answer"""
        answer = st.radio(
            "Choose an answer:",
            ["yes", "no"],
            index=["yes", "no"].index(st.session_state[f"user_answer_{index}"]) if st.session_state[f"user_answer_{index}"] else 0,
            key=f"question_{index}_radio"
        )
        st.session_state[f"user_answer_{index}"] = answer
        return answer, answer == question["answer"]

    def saveuserprogress(self):
        """Format for saving user data"""
        data = {
            "username": self.username,
            "score": self.score,
            "time_taken": self.time_taken,
            "answers": self.user_answers
        }

        # Save to JSON file with the method to check if it exits and is empty
        filename = "user_results.json"
        existing_data = []
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []

        existing_data.append(data)
        with open(filename, "w") as f:
            json.dump(existing_data, f, indent=4) #saved Json file format

    def leaderboard(self): # function to display who is leading in the quiz
        filename = "user_results.json"
        if os.path.exists(filename):#checking if file path exists
            with open(filename, "r") as f:# reading the file holding user's progress
                data = json.load(f)
            sorted_data = sorted(data, key=lambda x: x['score'], reverse=True)#sorting user scores with the highest score at the top
            st.subheader("🏅 Leaderboard") #subheader in webapp using streamlit
            for idx, entry in enumerate(sorted_data[:10], start=1):# indexing users and their score from the top 10 users only
                st.markdown(f"**{idx}. {entry['username']}** — Score: {entry['score']}, Time: {entry['time_taken']:.2f}s") # sttreamlit markdown in the webapp
        else:
            st.info("No quiz data found.") # output if no users quiz data is available
