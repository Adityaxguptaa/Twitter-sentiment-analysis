import streamlit as st
import pickle
import time
import random
import plotly.graph_objects as go
import re


model = pickle.load(open('twitter_sentiment.pkl', 'rb'))

def preprocess_tweet(tweet):
    """Preprocess the tweet text to match model training."""
    tweet = tweet.lower()  
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE) 
    tweet = re.sub(r'\@\w+|\#', '', tweet)  
    tweet = re.sub(r'[^\w\s]', '', tweet)  
    tweet = re.sub(r'\d+', '', tweet)  
    tweet = tweet.strip()  
    return tweet



st.set_page_config(
    page_title="Twitter Sentiment Analysis",
    page_icon="🐦",
    layout="wide",  
    initial_sidebar_state="expanded",
)


st.markdown("""
    <style>
        /* Button hover effect */
        .stButton > button:hover {
            background-color: #ff4b4b;
            color: white;
            transition: 0.3s;
        }
        /* Custom font */
        html, body, [class*="css"] {
            font-family: 'Arial', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: #1DA1F2;'>🐦 Twitter Sentiment Analysis</h1>
        <p style='font-size: 18px;'>Analyze and visualize the sentiment of tweets with predictions and insights.</p>
    </div>
""", unsafe_allow_html=True)


st.markdown("---")
tweet = st.text_input("💬 Enter your tweet below:", placeholder="Type a tweet here...")
submit = st.button("🚀 Predict Sentiment")


if "predictions" not in st.session_state:
    st.session_state.predictions = {"Positive": 0, "Negative": 0, "Neutral": 0}


if submit:
    if tweet.strip():
        with st.spinner("Analyzing sentiment..."):
            start = time.time()
            prediction = model.predict([tweet])
            end = time.time()

        
        sentiment = prediction[0].capitalize()  

        if sentiment in st.session_state.predictions:
            st.session_state.predictions[sentiment] += 1  

        
        if sentiment == "Positive":
            st.success(f"🌟 Sentiment: Positive")
        elif sentiment == "Negative":
            st.error(f"💔 Sentiment: Negative")
        elif sentiment == "Neutral":
            st.info(f"😐 Sentiment: Neutral")
        else:
            st.warning(f"⚠️ Unexpected sentiment detected: {sentiment}")

        st.write(f"⏳ **Prediction Time:** {round(end-start, 2)} seconds")
    else:
        st.warning("⚠️ Please enter a tweet before submitting!")


st.markdown("---")
st.header("📊 Sentiment Analytics")


labels = list(st.session_state.predictions.keys())
values = list(st.session_state.predictions.values())

fig = go.Figure(
    data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.3,  # Creates a donut-style chart
            pull=[0.1 if v > 0 else 0 for v in values],  # Highlight non-zero sections
            textinfo="label+percent",
            hoverinfo="label+value",
            marker=dict(colors=["#1DA1F2", "#FF4B4B", "#FFD700"]),
        )
    ]
)

fig.update_traces(
    hoverinfo="label+percent",
    textfont_size=14,
    marker=dict(line=dict(color="#000000", width=2)),
)

fig.update_layout(
    title="Sentiment Distribution (3D Pie Chart)",
    title_x=0.5,
    height=600,
    width=800,
)

st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center;'>
        <p style='color: gray;'>Created with ❤️ using Streamlit and plotly by ADITYA GUPTA</p>
    </div>
""", unsafe_allow_html=True)

# **Game Section**: Game Selection Menu
st.markdown("---")
st.header("🎮 Timepass: Choose a Game to Play!")

game_choice = st.radio("Pick a game to play:", ["Guess the Number", "Tic Tac Toe", "Hangman"])


if game_choice == "Guess the Number":
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    if not st.session_state.game_started:
        st.session_state.number_to_guess = random.randint(1, 100)
        st.session_state.game_started = True

   
    if st.session_state.game_started:
        guess = st.number_input("Guess a number between 1 and 100:", min_value=1, max_value=100, step=1)
        if st.button("Check Guess"):
            if guess < st.session_state.number_to_guess:
                st.write("Too low! Try again. 🔽")
            elif guess > st.session_state.number_to_guess:
                st.write("Too high! Try again. 🔼")
            else:
                st.write(f"🎉 Correct! The number was {st.session_state.number_to_guess}. You win! 🎉")
                st.session_state.game_started = False  
                st.balloons()  
    else:
        st.button("Start a New Game", on_click=lambda: st.session_state.update({"game_started": False}))


elif game_choice == "Tic Tac Toe":
    if 'tic_tac_toe' not in st.session_state:
        st.session_state.tic_tac_toe = ['' for _ in range(9)]  
        st.session_state.current_player = 'X'

    board = st.session_state.tic_tac_toe

    
    def check_winner():
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8], 
            [0, 4, 8], [2, 4, 6]  
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
                return board[combo[0]]
        return None

    
    st.write("**Tic Tac Toe Board:**")
    cols = st.columns(3)
    for i in range(9):
        if cols[i % 3].button(board[i] or ' ', key=i):
            if board[i] == '' and (not check_winner()):
                board[i] = st.session_state.current_player
                st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'

  
    winner = check_winner()
    if winner:
        st.write(f"🎉 Player {winner} wins! 🎉")
        st.session_state.tic_tac_toe = ['' for _ in range(9)]  
        st.balloons()


elif game_choice == "Hangman":
    if 'hangman' not in st.session_state:
        st.session_state.hangman_word = random.choice(['python', 'streamlit', 'machine', 'learning', 'data', 'science'])
        st.session_state.guesses = []
        st.session_state.chances = 6

    word = st.session_state.hangman_word
    guesses = st.session_state.guesses
    chances = st.session_state.chances

    
    display_word = ''.join([letter if letter in guesses else '_' for letter in word])
    st.write(f"**Word to Guess:** {display_word}")
    st.write(f"**Chances left:** {chances}")
    
    if display_word == word:
        st.write("🎉 Congratulations! You guessed the word! 🎉")
        st.session_state.hangman = {}  
        st.balloons()
    else:
        
        guess = st.text_input("Guess a letter:", max_chars=1)
        if guess and guess.isalpha() and guess not in guesses:
            guesses.append(guess)
            if guess not in word:
                st.session_state.chances -= 1
            if st.session_state.chances == 0:
                st.write(f"❌ You lost! The word was {word}. ❌")
                st.session_state.hangman = {}  
