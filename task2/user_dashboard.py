import streamlit as st
import pandas as pd
import os
import json
import re
from collections import Counter
from dotenv import load_dotenv
from groq import Groq

# -------------------------------
# LLM setup (Groq)
# -------------------------------
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

DATA_FILE = "feedback.csv"

def init_data_file():
    if not os.path.exists(DATA_FILE):
        df_empty = pd.DataFrame(
            columns=["rating", "review", "ai_response", "ai_summary", "ai_action"]
        )
        df_empty.to_csv(DATA_FILE, index=False)

def load_data():
    if not os.path.exists(DATA_FILE):
        init_data_file()
    return pd.read_csv(DATA_FILE)

def parse_json_safely(text: str):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1:
        cleaned = cleaned[start:end+1]
    return json.loads(cleaned)

def call_llm_for_feedback(rating: int, review: str):
    prompt = f"""
You are an AI assistant in a customer feedback system.

User has submitted a review and a star rating.

Review: "{review}"
Rating: {rating}

Return ONLY valid JSON in this exact format:
{{
  "ai_response": "<short friendly reply to the user>",
  "ai_summary": "<one-line summary of the review>",
  "ai_action": "<recommended next action for the business>"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    raw = response.choices[0].message.content
    data = parse_json_safely(raw)
    return data  # dict with ai_response, ai_summary, ai_action

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("⭐ User Feedback Portal")
st.write("Submit your rating and review. Our AI will respond and help the business improve.")

rating = st.slider("Select Rating:", 1, 5, 3)
review = st.text_area("Write your review:")

if st.button("Submit"):
    if not review.strip():
        st.warning("Please write a review before submitting.")
    else:
        with st.spinner("Generating AI response..."):
            try:
                ai_data = call_llm_for_feedback(rating, review)

                # Load existing data
                df = load_data()

                # Append new row
                new_row = {
                    "rating": rating,
                    "review": review,
                    "ai_response": ai_data.get("ai_response", ""),
                    "ai_summary": ai_data.get("ai_summary", ""),
                    "ai_action": ai_data.get("ai_action", ""),
                }

                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)

                st.success("✅ Your review has been submitted!")

                st.subheader("💬 AI Response")
                st.write(ai_data.get("ai_response", ""))

                st.subheader("📝 AI Summary")
                st.write(ai_data.get("ai_summary", ""))

                st.subheader("📌 Recommended Action")
                st.write(ai_data.get("ai_action", ""))
            except Exception as e:
                st.error(f"Something went wrong while calling the AI: {e}")

