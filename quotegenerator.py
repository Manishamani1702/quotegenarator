import streamlit as st
import json
import random
import together
from PIL import Image

# Set your Together AI key
TOGETHER_API_KEY = "Enter your api key " #add your api key here
together.api_key = TOGETHER_API_KEY

# Load fallback local quotes
def load_quotes():
    with open("quotes.json", "r") as f:
        return json.load(f)

# Generate quote using Together AI
def generate_quote_with_ai(mood):
    prompt = f"Generate a short motivational quote for someone feeling {mood}."
    try:
        response = together.Complete.create(
            prompt=prompt,
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            max_tokens=60
        )
        return response["choices"][0]["text"].strip()
    except:
        return None

# Get quote based on mood (fallback to local if AI fails)
def get_quote(mood):
    ai_quote = generate_quote_with_ai(mood)
    if ai_quote:
        return ai_quote
    else:
        quotes = load_quotes()
        filtered = [q["quote"] for q in quotes if q["category"] == mood.lower()]
        return random.choice(filtered) if filtered else "No quote found for that mood."

# Streamlit UI
st.set_page_config(page_title="💬 AI Quote Generator", page_icon="💬", layout="centered")

# Optional: add a banner or icon
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color:#6C63FF;'>AI-Powered Quote Generator</h1>
        <p style='font-size:18px;'>Get a motivational quote based on your mood or keyword</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Input box
mood = st.text_input("Enter your mood or a keyword (e.g., happy, anxious, focus):")

# Button and result area
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("✨ Generate Quote", use_container_width=True):
        if mood.strip() == "":
            st.warning("Please enter a mood or keyword.")
        else:
            quote = get_quote(mood)
            st.markdown("""
                <div style='background-color:#f0f2f6;padding:20px;border-radius:10px;margin-top:20px;'>
                    <h3 style='color:#333;'>💡 Here's your quote:</h3>
                    <blockquote style='font-size:20px; color:#555;'>❝ {} ❞</blockquote>
                </div>
            """.format(quote), unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 14px;'>Made with ❤️ using Streamlit & Together AI</p>
""", unsafe_allow_html=True)
