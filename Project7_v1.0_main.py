import streamlit as st
import random
from hangman_words_day7 import word_list
from logo_day7 import logo

# ================== GAME DATA ==================
st.title("🎯 Hangman Game")
st.text(logo)

stages = [
r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========''',
r'''
  +---+
  |   |
      |
      |
      |
      |
========='''
]

# ================== SESSION STATE ==================
if "choice" not in st.session_state:
    st.session_state.choice = random.choice(word_list)
    st.session_state.lives = 6
    st.session_state.res = []
    st.session_state.game_over = False

choice = st.session_state.choice
lives = st.session_state.lives
# res = st.session_state.res  <-- This local assignment was the culprit

# ================== DISPLAY PLACEHOLDER ==================
display = ""
for letter in choice:
    # Use st.session_state.res directly to ensure the UI stays updated
    display += letter if letter in st.session_state.res else "_"
st.subheader(display)

st.text(f"❤️ Lives Left: {lives}/6")
st.text(stages[lives])

# ================== USER INPUT ==================
if not st.session_state.game_over:
    guess = st.text_input("Enter your guess letter:", max_chars=1, key="input_guess")
    if st.button("Guess"):
        if not guess:
            st.warning("Please enter a letter")
        elif guess in st.session_state.res:
            st.info(f"You already guessed '{guess}'")
        else:
            st.session_state.res.append(guess)
            if guess not in choice:
                st.session_state.lives -= 1
                st.error(f"'{guess}' is not in the word!")

            # Check win/lose
            if st.session_state.lives == 0:
                st.session_state.game_over = True
                st.error(f"💀 YOU LOSE! The word was: **{choice}**")
            elif "_" not in "".join([l if l in st.session_state.res else "_" for l in choice]):
                st.session_state.game_over = True
                st.success("🎉 YOU WIN!")

            st.rerun()

# ================== RESTART ==================
if st.session_state.game_over:
    if st.button("🔄 Restart Game"):
        st.session_state.choice = random.choice(word_list)
        st.session_state.lives = 6
        st.session_state.res = []
        st.session_state.game_over = False
        st.rerun()

