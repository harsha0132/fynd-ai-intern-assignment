import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re
import os

DATA_FILE = "feedback.csv"

st.title("🛠 Admin Feedback Analytics Dashboard")
st.write("Monitor user feedback, AI summaries, and recommended actions.")

# -------------------------------
# Load data
# -------------------------------
if not os.path.exists(DATA_FILE):
    st.warning("No feedback data found yet. Ask users to submit reviews in the User Dashboard.")
else:
    df = pd.read_csv(DATA_FILE)

    if df.empty:
        st.warning("Feedback file is empty. Wait for some user submissions.")
    else:
        # -------------------------------
        # Filter slider
        # -------------------------------
        rating_filter = st.slider("Filter reviews by rating:", 1, 5, (1, 5))
        df_filtered = df[
            (df["rating"] >= rating_filter[0]) & (df["rating"] <= rating_filter[1])
        ]

        if df_filtered.empty:
            st.warning("No reviews in this rating range. Adjust the slider.")
        else:
            # -------------------------------
            # KPIs
            # -------------------------------
            avg_rating = df_filtered["rating"].mean()
            total_reviews = len(df_filtered)
            five_star_ratio = (df_filtered["rating"] == 5).mean() * 100

            col1, col2, col3 = st.columns(3)
            col1.metric("⭐ Average Rating", round(avg_rating, 2))
            col2.metric("📦 Total Reviews", total_reviews)
            col3.metric("🌟 % 5-Star Reviews", f"{five_star_ratio:.1f}%")

            # -------------------------------
            # Rating distribution
            # -------------------------------
            st.subheader("📌 Rating Distribution")

            fig, ax = plt.subplots()
            sns.countplot(x=df_filtered["rating"], ax=ax)
            ax.set_xlabel("Star Rating")
            ax.set_ylabel("Count")
            st.pyplot(fig)

            # -------------------------------
            # Word cloud based on reviews
            # -------------------------------
            st.subheader("☁️ Word Cloud of Reviews")

            all_text = " ".join(df_filtered["review"].dropna().tolist())
            if all_text.strip():
                wordcloud = WordCloud(
                    width=800, height=400, background_color="white"
                ).generate(all_text)

                fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
                ax_wc.imshow(wordcloud, interpolation="bilinear")
                ax_wc.axis("off")
                st.pyplot(fig_wc)
            else:
                st.info("Not enough text to generate a word cloud.")

            # -------------------------------
            # Review length distribution
            # -------------------------------
            st.subheader("📝 Review Length Distribution")

            df_filtered["word_count"] = df_filtered["review"].apply(
                lambda x: len(str(x).split())
            )

            fig_wc2, ax_wc2 = plt.subplots()
            sns.histplot(df_filtered["word_count"], bins=30, ax=ax_wc2)
            ax_wc2.set_xlabel("Word Count")
            ax_wc2.set_ylabel("Number of Reviews")
            st.pyplot(fig_wc2)

            # -------------------------------
            # Most frequent words
            # -------------------------------
            st.subheader("🔤 Most Frequent Words in Reviews")

            def clean_text(t):
                t = str(t).lower()
                t = re.sub(r"[^a-zA-Z\s]", "", t)
                return t

            words = " ".join(df_filtered["review"].apply(clean_text)).split()
            if words:
                common_words = Counter(words).most_common(20)
                word_df = pd.DataFrame(common_words, columns=["word", "count"])

                fig_fw, ax_fw = plt.subplots()
                sns.barplot(x="count", y="word", data=word_df, ax=ax_fw)
                ax_fw.set_xlabel("Frequency")
                ax_fw.set_ylabel("Word")
                st.pyplot(fig_fw)
            else:
                st.info("Not enough words to show frequency chart.")

            # -------------------------------
            # Show detailed table
            # -------------------------------
            st.subheader("📄 Recent Feedback with AI Insights")
            st.dataframe(
                df_filtered[
                    ["rating", "review", "ai_summary", "ai_action", "ai_response"]
                ].tail(20)
            )


