import streamlit as st
import random
from hangman_words_day7 import word_list
from logo_day7 import logo

# ================== GAME DATA ==================
st.title("🎯 Hangman Game")
st.code(logo) # Use st.code for the logo to prevent mobile formatting issues

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

# ================== DISPLAY PLACEHOLDER ==================
# We add spaces between underscores for better visibility on mobile screens
display = ""
for letter in choice:
    display += f"{letter} " if letter in st.session_state.res else "_ "

st.subheader("Word to guess:")
st.code(display) # st.code ensures underscores don't merge on mobile

st.text(f"❤️ Lives Left: {lives}/6")
st.code(stages[lives])

# ================== USER INPUT ==================
if not st.session_state.game_over:
    # .lower() ensures the game isn't case-sensitive
    guess = st.text_input("Enter your guess letter:", max_chars=1, key="input_guess").lower()
    
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

            # Re-calculate display for win/loss check
            current_display = "".join([l if l in st.session_state.res else "_" for l in choice])

            # Check win/lose
            if st.session_state.lives == 0:
                st.session_state.game_over = True
            elif "_" not in current_display:
                st.session_state.game_over = True
            
            st.rerun() 

# ================== END GAME SCREEN ==================
if st.session_state.game_over:
    if st.session_state.lives == 0:
        st.error(f"💀 YOU LOSE!")
        st.info(f"The correct word was: {choice.upper()}")
    else:
        st.success(f"🎉 YOU WIN! The word was indeed: {choice.upper()}")
        
    if st.button("🔄 Restart Game"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
