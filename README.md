Fynd AI Intern – Assignment Submission

Author: R. Sriharsha

Overview

This repository contains my submission for the Fynd AI Intern take-home assignment.
The assessment includes two parts:

Task 1: Predict Yelp ratings using review text

Task 2: Build Streamlit dashboards for users and admins

Both tasks were completed as described below.

## Project Structure

```
fynd-ai-intern-assignment/
│
├── task1/
│   └── rating_prediction.ipynb
│
├── task2/
│   ├── dashboard.py
│   ├── user_dashboard.py
│   ├── feedback.csv
│   └── requirements.txt
│
├── screenshots/
│   └── (dashboard images)
│
├── reports.pdf
└── README.md
```

Task 1 – Yelp Rating Prediction

For the prediction task, I used the Groq Llama 3.3–70B Versatile model to interpret each review and return a rating from 1 to 5.

Results

MSE: 0.635

R² Score: 1.0

How it works

A small wrapper function formats the review text into a prompt, sends it to the LLM, and returns the predicted rating. The model showed strong sentiment understanding and produced accurate predictions.

Task 2 – Streamlit Dashboards
User Dashboard

Users can:

Select a rating

Enter a review

Receive AI summaries and recommendations

Submit the entry (saved automatically in feedback.csv)

Run with:

streamlit run user_dashboard.py

Admin Dashboard

The admin dashboard provides:

Basic KPIs

Rating distribution

Word cloud

Review length distribution

Frequent-word analysis

Rating filter

Table of all user submissions

Run with:

streamlit run dashboard.py

Installation

Install required packages:

pip install -r requirements.txt

Screenshots

All screenshots of the dashboards are available in the /screenshots folder.

Final Notes

This project helped me explore:

NLP using LLMs

API-based model integration

Streamlit dashboard development

Basic data engineering

GitHub workflows

I enjoyed working on this assignment and gained valuable hands-on experience.

Repository Link
https://github.com/harsha0132/fynd-ai-intern-assignment

User Dashboard 
https://fynd-ai-intern-assignment-4pcxfsaxdycyo9o6w4th7e.streamlit.app/

Admin Dashboard
https://fynd-ai-intern-assignment-ttsjehtklkyqvhxmfuzbb7.streamlit.app/

Project Report
Included as reports.pdf in the repository.
