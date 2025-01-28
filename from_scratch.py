import random
import time
import streamlit as st
from wonderwords import RandomWord
from registration_page import registration_page
from login_page import login_page


def reset_session():
    # initialize session states
    st.session_state.current_page = "Home"
    st.session_state.number_memory_score = 0
    st.session_state.number_memory_level = 1
    st.session_state.number_memory_timer = 3
    st.session_state.word_memory_score = 0
    st.session_state.word_memory_lives = 3
    st.session_state.word_memory_seen = []
    st.session_state.word_memory_word_list = []


if "current_page" not in st.session_state:
    reset_session()


def homescreen():
    st.image("https://wiltgenlab.faculty.ucdavis.edu/wp-content/uploads/sites/210/2017/04/brain-banner.jpg")
    st.markdown("<h1 style='text-align: center; color: white;'>Memory Benchmark</h1>", unsafe_allow_html=True)
    st.subheader("Put your memory through its paces")
    st.write(
        """
        Welcome to the Memory Benchmark app! This app is designed to test and improve your memory skills with engaging games.

        - Test your ability to recall sequences in the **Number Game**.
        - Identify repeated and new words in the **Word Game**.

        Track your progress, challenge your memory, and have fun along the way!
        """
    )
    st.subheader("Navigation")
    st.write("Use the sidebar on the left to select a game and start playing.")


def number_memory():
    # initialize variables
    if "current_number" not in st.session_state:
        st.session_state.current_number = ""
    if "show_input" not in st.session_state:
        st.session_state.show_input = False

    # Title, score, level
    st.image(image="https://www.sparklebox.co.uk/wp-content/uploads/1-2049.jpg")
    st.markdown("<h1 style='text-align: center; color: white;'>Number Memory</h1>", unsafe_allow_html=True)
    st.write(f"**Score:** {st.session_state.number_memory_score}")
    st.write(f"**Level:** {st.session_state.number_memory_level}")

    # generate new number if necessary
    if st.session_state.current_number == "" and not st.session_state.show_input:
        st.session_state.current_number = "".join(
            [str(random.randint(0, 9)) for _ in range(st.session_state.number_memory_level)]
        )
        st.write(f"Remember this number: {st.session_state.current_number}")
        time.sleep(st.session_state.number_memory_timer)
        st.session_state.show_input = True

    # Show entry box after number vanished
    if st.session_state.show_input:
        st.empty()
        user_input = st.text_input("What was the number?", "")
        if st.button("Submit"):
            if user_input == st.session_state.current_number:
                st.success("Correct!")
                st.session_state.number_memory_score += 1
                st.session_state.number_memory_level += 1
                st.session_state.number_memory_timer += 0.5
            else:
                st.error(f"Wrong! The correct number was: {st.session_state.current_number}")
                st.write(f"You reached level {st.session_state.number_memory_level}")
                st.session_state.number_memory_score = 0
                st.session_state.number_memory_level = 1
                st.session_state.number_memory_timer = 3
            # Reset Number and start new round
            st.session_state.current_number = ""
            st.session_state.show_input = False


def word_memory():
    # Initialize variables
    if "word_memory_score" not in st.session_state:
        st.session_state.word_memory_score = 0  # score
    if "word_memory_lives" not in st.session_state:
        st.session_state.word_memory_lives = 3  # lives
    if "word_memory_seen_words" not in st.session_state:
        st.session_state.word_memory_seen_words = []  # seen words
    if "word_memory_current_word" not in st.session_state:
        st.session_state.word_memory_current_word = ""  # current word
    if "word_memory_word_pool" not in st.session_state:
        st.session_state.word_memory_word_pool = []  # list of random words

    # generate random word
    def generate_word():
        if not st.session_state.word_memory_word_pool:
            rw = RandomWord()
            st.session_state.word_memory_word_pool = [rw.word() for _ in range(50)]
        return random.choice(st.session_state.word_memory_word_pool)

    # Funktion zum Spiel-Reset
    def reset_game():
        st.session_state.word_memory_score = 0
        st.session_state.word_memory_lives = 3
        st.session_state.word_memory_seen_words = []
        st.session_state.word_memory_current_word = ""
        st.session_state.word_memory_word_pool = []

    # loose screen
    if st.session_state.word_memory_lives <= 0:
        st.title("You Lost!")
        st.subheader(f"Your final score: {st.session_state.word_memory_score}")

        if st.button("Play Again"):
            reset_game()
        return  # Stop game

    st.image(image="https://as2.ftcdn.net/jpg/01/42/89/99/1000_F_142899942_BJ9qtVpCEXdGpYHA9ZzhTTpBUY0ei6zj.jpg")
    st.markdown("<h1 style='text-align: center; color: white;'>Word Memory</h1>", unsafe_allow_html=True)
    st.write(f"**Score:** {st.session_state.word_memory_score}")
    st.write(f"**Lives:** {st.session_state.word_memory_lives}")

    # generate new word
    if not st.session_state.word_memory_current_word:
        st.session_state.word_memory_current_word = generate_word()

    # show current word
    st.write(f"Current Word:{st.session_state.word_memory_current_word}")

    # Buttons next to each other
    col1, col2 = st.columns(2)

    # New Button
    with col1:
        if st.button("New"):
            if st.session_state.word_memory_current_word in st.session_state.word_memory_seen_words:
                st.error("Wrong! This word has already been seen.")
                st.session_state.word_memory_lives -= 1
            else:
                st.success("Correct! New word added.")
                st.session_state.word_memory_seen_words.append(st.session_state.word_memory_current_word)
                st.session_state.word_memory_score += 1

            # generate word
            st.session_state.word_memory_current_word = generate_word()

    # Seen Button
    with col2:
        if st.button("Seen"):
            if st.session_state.word_memory_current_word in st.session_state.word_memory_seen_words:
                st.success("Correct! This word has already been seen.")
                st.session_state.word_memory_score += 1
            else:
                st.error("Wrong! This word has not been seen before.")
                st.session_state.word_memory_lives -= 1

            # Generate word
            st.session_state.word_memory_current_word = generate_word()


def stats():
    st.write("hello")


options = ["Home", "Login", "Register", "Number Memory", "Word Memory", "Statistics"]
page_selection = st.sidebar.radio("Choose", options)
if page_selection == "Home":
    homescreen()
elif page_selection == "Login":
    login_page()
elif page_selection == "Register":
    registration_page()
elif page_selection == "Number Memory":
    number_memory()
elif page_selection == "Word Memory":
    word_memory()
elif page_selection == "Statistics":
    stats()
