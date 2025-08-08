#importing necessary modules
import streamlit as st
import time
import random
from quizapplication import QuizApp

st.set_page_config(page_title="Quiz App", layout='centered')
st.title("🧠Quiz App")



if 'quizapp' not in st.session_state:
    st.session_state.quizapp = QuizApp()

quizapp = st.session_state.quizapp

if 'username' not in st.session_state:
    username = st.text_input("Enter your username:")
    if username:
        st.session_state.username = username
        quizapp.username = username
        quizapp.adduser(username)
        st.success(f"Welcome {username}!")
        st.rerun()
else:
    st.write(f"👤 Logged in as: **{st.session_state.username}**")
    quizapp.username = st.session_state.username

# Load questions only once
if 'questions_loaded' not in st.session_state:
    if st.button("📥 Load Questions"):
        quizapp.load_questions("opensource_questions.json")
        if quizapp.questions:
            st.session_state.questions_loaded = True
            st.success("✅ Questions loaded!")
        else:
            st.error("❌ Questions file not found.")

# Starting the Quiz
if st.session_state.get('questions_loaded') and 'quiz_started' not in st.session_state:
    if st.button("▶️ Start Quiz"):
        random.shuffle(quizapp.questions)
        st.session_state.quiz_started = True
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()


if st.session_state.get("quiz_started"):
    q_index = st.session_state.current_question
    if q_index < len(quizapp.questions):
        question = quizapp.questions[q_index]
        answer, correct = quizapp.ask_question(question, q_index)

        if st.button("✅ Submit Answer"):
            if answer:
                if correct:
                    st.success("Correct!")
                    st.session_state.score += 1
                else:
                    st.error("Wrong!")
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.warning("Please select an answer before submitting.")

        if st.button("🛑 Stop Quiz"):
            quizapp.score = st.session_state.score
            quizapp.time_taken = time.time() - st.session_state.start_time
            quizapp.saveuserprogress()

            st.info(f"⏹ Quiz exited early.\n\nScore: **{quizapp.score} / {len(quizapp.questions)}**")
            st.info(f"⏱ Time taken: **{quizapp.time_taken:.2f} seconds**")

            for key in ['quiz_started', 'current_question', 'start_time']:
                st.session_state.pop(key, None)
            st.stop()

    else:
        quizapp.score = st.session_state.score
        quizapp.time_taken = time.time() - st.session_state.start_time
        quizapp.save_user_progress()

        st.success(f"🎉 Quiz complete! Score: **{quizapp.score} / {len(quizapp.questions)}**")
        st.info(f"⏱ Time taken: **{quizapp.time_taken:.2f} seconds**")

        for key in ['quiz_started', 'current_question', 'start_time']:
            st.session_state.pop(key, None)

# Show Leaderboard
if st.button("🏆 Show Leaderboard"):
    quizapp.leaderboard()
