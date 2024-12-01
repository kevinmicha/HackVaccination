import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from PIL import Image
import os
import altair as alt

st.set_page_config(page_title="Action Review Dashboard", layout="wide")

##################################################

def set_past_action_date():
    try:
        with open("current_action.txt", "r") as f:
            st.session_state.past_action_date = f.readline()
    except:
        st.session_state.past_action_date = "May 31st 2023"
        
if 'past_action_date' not in st.session_state:
    set_past_action_date() ## Default date. Would get this from Incident Reports

if "past_trigger_dates" not in st.session_state:
    st.session_state.past_trigger_dates = ["May 31st 2023", "July 28th 2023"]
    # st.session_state.past_trigger_dates = []
    # for i in os.listdir("Incident_Reports"):
    #     st.session_state.past_trigger_dates.append(i.replace("_", " "))

##################################################
# Load Data
##################################################

@st.cache_data
def get_page_data():
    loc = os.path.join(os.getcwd(), "/Incident_Reports/", st.session_state.action_date)
    # images = ...
    # text = ...

##################################################
# Initialise Example Data
past_action_images = ["https://i.ibb.co/ZN7GnhN/Screenshot-from-2024-12-01-09-19-15.png", 
                        "https://i.ibb.co/XsTk9Kt/Screenshot-from-2024-12-01-09-17-58.png", 
                        "https://i.ibb.co/48xrJzD/image-antivax.png"]



# Mock Data

tweet_text = """🚫 No scientific evidence links vaccines to Alzheimer’s disease. Vaccines protect against infections that can lead to inflammation, a risk factor for Alzheimer’s. They're part of preventive health, not a cause of neurological diseases.
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


##################################################
# Chart Data
##################################################
#Get data for 2 weeks before date and a month after date

#Types

date = pd.to_datetime(st.session_state.past_action_date)
st.session_state.display_data.Time = pd.to_datetime(st.session_state.display_data.Time)

chart_data = st.session_state.display_data[st.session_state.display_data["Sentiment"]=="Negative"].groupby(st.session_state.display_data.Time.dt.date)[['Engagements', "Likes", "Retweets", "Comments"]].sum().reset_index()

chart_data["Time"] = pd.to_datetime(chart_data["Time"])
chart_data = chart_data[(chart_data.Time.dt.date > date.date() - pd.Timedelta(days=14)) &
                        (chart_data.Time.dt.date < date.date() + pd.Timedelta(days=30))]

chart_engagement = (
    (
        alt.Chart(chart_data)
        .mark_line(color="blue")
        .encode(
            x=alt.X(
                "Time",
                type="temporal",
            ),
            y=alt.Y(
                field="Engagements",
                type="quantitative",
                aggregate="sum",
                title="Engagements"
            ),
            # color=alt.Color(
            #     "region",
            #     type="nominal",
            #     title="Regions",
            #     scale=alt.Scale(domain=regions, range=colors),
            #     legend=alt.Legend(
            #         direction="vertical",
            #         symbolType="triangle-left",
            #         tickCount=4,
            #     ),
            # ),
        )
    )
    .properties(width=600)#Rolling mean 
)


rolling_average = (
    (
        alt.Chart(chart_data)
        .mark_line(color='red')
        .transform_window(rolling_mean='mean(Engagements)', frame=[-2, 2])
        .encode(
            x=alt.X(
                "Time",
                type="temporal",
            ),
            y=alt.Y(
                field="rolling_mean",
                type="quantitative",
                title="Engagements"
            )
            # color=alt.Color(
            #     "region",
            #     type="nominal",
            #     title="Regions",
            #     scale=alt.Scale(domain=regions, range=colors),
            #     legend=alt.Legend(
            #         direction="vertical",
            #         symbolType="triangle-left",
            #         tickCount=4,
            #     ),
            # ),
        )
    )
    .properties(width=600, height = 450)#Rolling mean 
)

scatter_data = chart_data[chart_data.Time.dt.date == date.date()]

scatter = ( 
    alt.Chart(scatter_data).mark_circle(size = 100).encode(
            x=alt.X(
                "Time",
                type="temporal",
            ),
            y=alt.Y(
                field="Engagements",
                type="quantitative",
                aggregate="sum",
                title="Engagements"
            ),
    )
)

plot_fig =   chart_engagement + rolling_average + scatter

##################################################
# Page Layout
##################################################
# Layout
st.title("Action Review Dashboard")
st.subheader("Date: " + str(st.session_state.past_action_date))

# def set_new_past_action():
#     #write out action_drop_down
#     try:
#         with open("current_action.txt", "w") as f:
#             f.write(action_drop_down, "w")
#     except:
#         pass
#     set_past_action_date()

#action_drop_down = st.selectbox("Select Date", st.session_state.past_trigger_dates)#, on_change=set_new_past_action()) Need to figure out how to trigger data loading on_change.

# Bottom Layout
col3, col4 = st.columns([3, 2], gap="large")

with col3:
    st.markdown("### 📈 Engagement Over Time")

    # Create the plot
    st.altair_chart(plot_fig)    

with col4:
    st.markdown("### 🌟 Engagement Stats")
    st.write("The chart on the left shows the daily negative engagements two weeks before the action date and a month after the action date. The figures below show the total engagements with the tweet that was posted.")

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

st.subheader("Trigger Tweets")
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://i.ibb.co/ZN7GnhN/Screenshot-from-2024-12-01-09-19-15.png", use_container_width=True)

with col2:
    st.image("https://i.ibb.co/XsTk9Kt/Screenshot-from-2024-12-01-09-17-58.png", use_container_width=True)

with col3:
    st.image("https://i.ibb.co/48xrJzD/image-antivax.png", use_container_width=True)

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

