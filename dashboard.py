import streamlit as st
import altair as alt
import requests
import asyncio
import threading
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import colorsys
from wordcloud import WordCloud
import os
import copy

st.set_page_config(page_title="Agent Interaction Dashboard", layout="wide")


if "site_loc_action" not in st.session_state:
    st.session_state.site_loc_action = "pages/Action_Response.py"
if "site_loc_past_action" not in st.session_state:
    st.session_state.site_loc_past_action = "pages/Review_Past_Actions.py"

if "engagement_action_trigger" not in st.session_state:
    st.session_state.engagement_action_trigger = 35000

if "sentiment_action_trigger" not in st.session_state:
    st.session_state.sentiment_action_trigger = 0.55

if "past_trigger_dates" not in st.session_state:
    st.session_state.past_trigger_dates = ["May 31st 2023", "July 28th 2023"]
    # st.session_state.past_trigger_dates = []
    # for i in os.listdir("Incident_Reports"):
    #     st.session_state.past_trigger_dates.append(i.replace("_", " "))

############################################
# Get Data Functions
############################################
@st.cache_data
def get_data():
    #data = pd.read_csv("df_simulated_tweets.csv")
    data = pd.read_csv("df_simulated_tweets_all.csv")
    data["Engagements"] = data["Retweets"] + data["Likes"] + data["Comments"]
    #Set time type to datetime
    data["Time"] = pd.to_datetime(data["Time"])
    return data

@st.cache_data
def get_feature_presets():
    feature_presets = pd.read_csv("pages/feature_presets.csv")
    return feature_presets

@st.cache_data
def get_world_map():
    world_map = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    return world_map

def set_trigger_action():
    #Check if the number of engagements in the last 7 days is less than 1000
    data_last7days = st.session_state.display_data[st.session_state.display_data.Time.dt.date > st.session_state.display_data.Time.dt.date.max() - pd.Timedelta(days=7)]

    if data_last7days[data_last7days["Sentiment"] == "Negative"]["Engagements"].sum() > st.session_state.engagement_action_trigger:
        st.session_state.action_trigger = True
        st.session_state.action_trigger_type = "Engagement"
    else:
        if (data_last7days["Engagements"].sum() > st.session_state.engagement_action_trigger*0.5) & (data_last7days[data_last7days["Sentiment"] == "Negative"]["Engagements"].sum()/data_last7days["Engagements"].sum() > st.session_state.sentiment_action_trigger):
            st.session_state.action_trigger = True
            st.session_state.action_trigger_type = "Sentiment"
        else:
            st.session_state.action_trigger = False
############################################
# Initialise Data
############################################
### Filter Tab Creation



############################################

if "world_map" not in st.session_state:
    st.session_state.world_map = get_world_map()

if "display_data" not in st.session_state:
    st.session_state.display_data = get_data()

if "todays_date" not in st.session_state:
    st.session_state.todays_date = st.session_state.display_data.Time.max()

if "action_trigger" not in st.session_state:
    st.session_state.action_trigger = False
    st.session_state.action_trigger_type = None
    set_trigger_action()

############################################
#Generate Map
############################################
#Groupby location
subset = st.session_state.display_data.groupby("Location", )[['Retweets', 'Likes', 'Comments', 'Engagements']].sum()

#In data map location to iso_a3
subset['iso_a3'] = subset.index.map({'UK': 'GBR', 'USA': 'USA', 'Canada': 'CAN', 'India': 'IND', 'Australia': 'AUS', 'Germany': 'DEU'})
world_subset = st.session_state.world_map[st.session_state.world_map['iso_a3'].isin(['GBR', 'USA', 'CAN', 'IND', 'AUS', 'DEU'])]

subset = pd.merge(world_subset, subset, on='iso_a3', how='left')
subset['colour'] = subset['Engagements']/subset['Engagements'].max()
subset["RGB"] = subset['colour'].apply(lambda x: list(colorsys.hsv_to_rgb(0.5, x, 0.5)))

#Add a column to the world map for the number of engagements
world_map = st.session_state.world_map

layers = [
    pdk.Layer(
        "GeoJsonLayer",
        data=st.session_state.world_map,
        get_fill_color=[255, 120, 150],
    ),
    pdk.Layer(
        "GeoJsonLayer", 
        data = subset, 
        get_fill_color = "[255*RGB[0], 255*RGB[1], 255*RGB[2]]",
    ),
]

############################################
# Generate Word Cloud
############################################
#Word Cloud Words from last week of data

#Subset data to last week
data_last7days = st.session_state.display_data[st.session_state.display_data.Time.dt.date > st.session_state.display_data.Time.dt.date.max() - pd.Timedelta(days=7)]

words = data_last7days["Keywords"].str.split(expand=True).stack().apply(lambda x: x.strip(","))
w_cloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(words))

############################################
# Generate Charts
############################################

date1 = pd.to_datetime("May 31st 2023")
date2 = pd.to_datetime("July 28th 2023")

#Sum Engagements for each day
engagement_data = st.session_state.display_data[st.session_state.display_data["Sentiment"]=="Negative"].groupby(st.session_state.display_data.Time.dt.date)[['Engagements', "Likes", "Retweets", "Comments"]].sum().reset_index()
engagement_data["Time"] = pd.to_datetime(engagement_data["Time"])

#engagement data on date 1
scatter_data1 = engagement_data[engagement_data["Time"].dt.date == date1.date()]
scatter_data2 = engagement_data[engagement_data["Time"].dt.date == date2.date()]
scatter_data = pd.concat([scatter_data1, scatter_data2])

chart_engagement = (
    (
        alt.Chart(engagement_data)
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
        alt.Chart(engagement_data)
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


############################################
# Generate Page
############################################


st.title("Agent Interaction Dashboard")
if st.session_state.action_trigger:
    st.subheader("Welcome to the Agent Interaction Dashboard - Urgent Action Recommended!!")
else:
    st.subheader("Welcome to the Agent Interaction Dashboard.")

st.write("This dashboard provides insights into the sentiment of tweets related to vaccines and the engagement levels of these tweets. The map below shows the location of tweets and the word cloud shows the most common words used in the last week of tweets.")

data_col, action_col = st.columns(spec = [3, 2])

with data_col:
    st.header("Negative Sentiments Over Time")
    st.write("The chart below shows the number of Engagements per day for tweets with negative sentiment over time alongside a 5 day rolling average.")

    st.altair_chart(plot_fig) # chart_engagement)

    st.session_state.display_data['Engagements_Rolling'] = st.session_state.display_data['Engagements'].rolling(window=2000).mean()
    #st.line_chart(st.session_state.display_data, x = "Time", y = "Engagements_Rolling")


with action_col:
    st.header("Actions")

    if st.session_state.action_trigger:
        st.subheader("Recommended Action!")
        if st.session_state.action_trigger_type == "Engagement":
            st.write("Based on the engagement analysis, there's a high focus on vaccines right now! It is a good time to send out a tweet to engage with the conversation.")
        else:
            st.write("Based on the sentiment analysis, negative tweets are overwhelming the conversation. It is a good time to send out a tweet to counteract the negative sentiment.")
        st.page_link(st.session_state.site_loc_action, label = "Review Recommended Tweet Here")#

    else:
        st.subheader("No Action Required")
        st.write("Based on the sentiment analysis, no action is required at this moment")

    st.subheader("Past Actions")
    action_date = st.selectbox("Review Past Action", ["Past Actions", "Action: May 31st 2023", "Action: July 28th 2023"])

    if action_date != "Past Actions":
        st.write(f"Action Date: {action_date[8:]}")
        st.write(f'Trigger Type: Negative Sentiments.') #Should get this from folder.
        st.write("Action Details: Post Made to Twitter")
        is_clicked = st.button("View Action Outcomes")
        if is_clicked:
            #write action_date to txt file
            with open("current_action.txt", "w") as f:
                f.write(action_date[8:])
            st.switch_page(st.session_state.site_loc_past_action)
        


data_col, action_col = st.columns(spec = [2, 2])

with data_col:

    st.subheader("Where are our relevant tweets coming from?")
    st.write("Engage with the map below to see where our tweets are coming.")
    st.pydeck_chart(pdk.Deck(layers, map_provider=None))

with action_col:
    st.subheader("What are people talking about?")

    st.write(f"Over {data_last7days.shape[0]} relevant tweets have been scraped in the last week, see what everyone's been talking about:")
    st.image(w_cloud.to_array(), use_container_width=True)



st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
