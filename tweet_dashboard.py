import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from PIL import Image

# Mock Data
tweet_text = """
🔍💉 Let's set the record straight on vaccines! Vaccines undergo rigorous testing to ensure their safety and efficacy before they are authorized for use. According to multiple studies, the known side effects of COVID-19 vaccines like those from Pfizer/BioNTech and Moderna are largely rare and well-documented.

The recent study highlighted that their benefits in preventing severe disease far outweigh these rare risks. Medical experts emphasize that the scientific consensus is clear: vaccines are safe, effective, and crucial in our fight against diseases like COVID-19, polio, and measles.

Misinformation can lead to hesitancy and risks for all of us. It's essential to rely on trusted sources of information about vaccine safety. Let's prioritize facts over fear! 

#VaccinesWork #TrustScience #HealthForAll
"""

tweet_date = "20 October 2024"

sources = [
    "Source 1: https://www.who.int/news-room/spotlight/history-of-vaccination/a-brief-history-of-vaccination",
    "Source 2: https://www.cdc.gov/vaccines/basics/explaining-how-vaccines-work.html",
    "Source 3: https://ourworldindata.org/covid-vaccinations",
]

# Mock time series data
dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(7)]
values = [50, 75, 125, 100, 150, 200, 180]

# Engagement data
replies = 10
reposts = 54
likes = 88

# Icons
reply_icon = "https://upload.wikimedia.org/wikipedia/commons/5/50/Twitter_Reply.png"
repost_icon = "https://cdn0.iconfinder.com/data/icons/interface-editing-and-time-1/64/retweet-arrow-twitter-512.png"
like_icon = "https://www.shareicon.net/data/512x512/2017/06/22/887576_heart_512x512.png"

# Page Configuration
st.set_page_config(page_title="Vaccine Myth-Busting Dashboard", layout="wide")

# Layout
st.title("📊 Vaccine Myth-Busting Dashboard")
st.subheader("Informative Tweets and Engagement Insights")

# Top Layout
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown("### 🔍 Informative Tweet")
    st.markdown(
        f"""
        <div style='background-color:#f9f9f9; padding:20px; border-radius:10px; position:relative;'>
            <p style='margin-bottom:30px;'>{tweet_text}</p>
            <div style='position:absolute; bottom:10px; right:20px; color:gray; font-size:12px;'>
                {tweet_date}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown("### 🔗 Sources")
    for source in sources:
        st.markdown(f"- [{source.split(': ')[1]}]({source.split(': ')[1]})")

# Bottom Layout
col3, col4 = st.columns([3, 2], gap="large")

with col3:
    st.markdown("### 📈 Engagement Over Time")

    # Generate date range for x-axis
    dates = pd.date_range(start="2023-10-20", periods=31)
    dates = dates.to_numpy()  # Convert to NumPy array to avoid multi-dimensional indexing issues

    # Generate sample data
    np.random.seed(42)  # For reproducibility
    negative_trend = np.linspace(100, 80, len(dates)) + np.random.normal(0, 2, len(dates))
    positive_trend = np.linspace(50, 70, len(dates)) + np.random.normal(0, 2, len(dates))

    # Create the plot
    fig, ax = plt.subplots(figsize=(10,6))

    # Plot lines
    ax.plot(dates, negative_trend, label="Negative", color="red", linewidth=2)
    ax.plot(dates, positive_trend, label="Positive", color="green", linewidth=2)

    # Add legend
    ax.legend(loc="upper right")

    # Add titles and labels
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Sentiment Score", fontsize=12)

    # Improve layout
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45)
    
    #fig, ax = plt.subplots()
    #ax.plot(dates, values, marker="o", linestyle="-")
    #ax.set_title("Engagement Over Time")
    #ax.set_ylabel("Engagement")
    #ax.set_xlabel("Date")
    
    st.pyplot(fig)

with col4:
    st.markdown("### 🌟 Engagement Stats")
    col_replies, col_reposts, col_likes = st.columns(3)
    with col_replies:
        st.image(reply_icon, width=50)
        st.metric("Replies", replies)
    with col_reposts:
        st.image(repost_icon, width=50)
        st.metric("Reposts", reposts)
    with col_likes:
        st.markdown(
            f"""
            <div style='display:flex; align-items:center; margin-left:-15px;'>
                <img src='{like_icon}' width='65' style='margin-right:10px;'/>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.metric("Likes", likes)