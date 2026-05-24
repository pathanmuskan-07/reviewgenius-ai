import streamlit as st
import google.generativeai as genai
import os

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

st.title("ReviewGenius AI 💬")

review = st.text_area("Enter customer review")

if st.button("Analyze"):
    if review:
        prompt = f"""
Analyze this review:
1. Sentiment
2. Summary
3. Suggestions

Review:
{review}
"""
        response = model.generate_content(prompt)
        st.write(response.text)
