import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import copy

@st.cache_data
def get_data():
    data = pd.read_csv("df_simulated_tweets.csv")
    return data

##In real life, this wouldn't exist and would just call from feature_presets.csv
@st.cache_data
def get_initial_feature_presets():
    feature_presets = pd.read_csv("pages/feature_presets_initial.csv", index_col = 0)
    return feature_presets

@st.cache_data
def get_feature_presets():
    feature_presets = pd.read_csv("pages/feature_presets.csv", index_col = 0)
    return feature_presets

#############################################
# Page Configuration

st.set_page_config(page_title="Interactive Graphs", layout="wide")

st.title("Filter Creation & Interaction")
st.session_state.raw_data = get_data()

#############################################
# Session State Initialization

st.session_state.filter_options = {"Sentiment": ["All", "Neutral", "Positive", "Negative"]}

if 'feature_presets' not in st.session_state:
    st.session_state.feature_presets = get_initial_feature_presets()

if "filter_sentiment" not in st.session_state:
    st.session_state.filter_sentiment = None

if "feature_new_preset" not in st.session_state:
    st.session_state.feature_new_preset = None

#############################################
### Filter Tab Creation

if "toggle_filter" not in st.session_state:
    st.session_state.toggle_filter = False  # Default to on

if "toggle_save" not in st.session_state:
    st.session_state.toggle_save = False

if "toggle_key_filter" not in st.session_state:
    st.session_state.toggle_key_filter = 1

if 'clicked_save' not in st.session_state:
    st.session_state.clicked_save = False

#############################################
## Functions associated with user events:

def save_clicked_off():
    st.session_state.clicked_save = False

def save_clicked_on():
    st.session_state.clicked_save = not st.session_state.clicked_save

def toggel_filter_toggle():
    st.session_state.toggle_filter = not st.session_state[st.session_state.toggle_key_filter]
    st.session_state.toggle_key_filter += 1

    update_data()

def save_preset():
    dict_presets = st.session_state.feature_presets
    dict_presets[st.session_state.feature_new_preset] = {"Sentiment": st.session_state.output_sentiment}
    dict_presets.to_csv("pages/feature_presets.csv")

def update_presets():
    st.session_state.filter_sentiment = st.session_state.feature_presets[st.session_state.feature_choice]["Sentiment"]

    # df.to_csv("pages/feature_presets.csv")

def update_data():
    st.session_state.display_data = st.session_state.raw_data.copy()
    if st.session_state.filter_sentiment != "All":
        st.session_state.display_data = st.session_state.display_data[st.session_state.display_data["Sentiment"] == st.session_state.filter_sentiment]

#############################################
###Filter Creation
filter_toggle = st.toggle("Show Filters", value=st.session_state.toggle_filter, key=st.session_state["toggle_key_filter"])

feature_drop_down = st.empty()

if filter_toggle:
    st.session_state.output_sentiment = feature_drop_down.selectbox("Tweet Sentiment", st.session_state.filter_options["Sentiment"])
    st.session_state.filter_sentiment = copy.deepcopy(st.session_state.output_sentiment)
    # if filter_region != "All":
    #     sales_data = sales_data[sales_data["region"] == filter_region]
    # region_options = ["All"] + regions

    save_toggle = st.toggle("Save Filtered Data", value =st.session_state.toggle_save)
    if save_toggle:
        # save_clicked_off()
        st.session_state.feature_new_preset = st.text_input("Save Title")
        save_button = st.button("Save", on_click=save_clicked_on)

if st.session_state.clicked_save:
    save_preset()
    # st.session_state.feature_choice = st.selectbox("Feature Presets", list(st.session_state.feature_presets.keys()), on_change = update_presets)

#############################################
# Select Preset Features
if not filter_toggle:
    st.session_state.feature_choice = feature_drop_down.selectbox("Feature Presets", list(st.session_state.feature_presets.keys()))
    update_presets()

#############################################
### Display Data

update_data()
st.line_chart(st.session_state.display_data, x = "Time", y = "Retweets")




# regions = ["LATAM", "EMEA", "NA", "APAC"]
# colors = [
#     "#aa423a",
#     "#f6b404",
#     "#327a88",
#     "#303e55",
#     "#c7ab84",
#     "#b1dbaa",
#     "#feeea5",
#     "#3e9a14",
#     "#6e4e92",
#     "#c98149",
#     "#d1b844",
#     "#8db6d8",
# ]
# months = [
#     "Jan",
#     "Feb",
#     "Mar",
#     "Apr",
#     "May",
#     "Jun",
#     "Jul",
#     "Aug",
#     "Sep",
#     "Oct",
#     "Nov",
#     "Dec",
# ]



# @st.cache_data
# def get_data():
#     dates = pd.date_range(start="1/1/2022", end="12/31/2022")
#     data = pd.DataFrame()
#     sellers = {
#         "LATAM": ["S01", "S02", "S03"],
#         "EMEA": ["S10", "S11", "S12", "S13"],
#         "NA": ["S21", "S22", "S23", "S24", "S25", "S26"],
#         "APAC": ["S31", "S32", "S33", "S34", "S35", "S36"],
#     }
#     rows = 25000
#     data["transaction_date"] = np.random.choice([str(i) for i in dates], size=rows)
#     data["region"] = np.random.choice(regions, size=rows, p=[0.1, 0.3, 0.4, 0.2])
#     data["transaction_amount"] = np.random.uniform(100, 250000, size=rows).round(2)
#     data["seller"] = data.apply(
#         lambda x: np.random.choice(sellers.get(x["region"])), axis=1
#     )
#     return data.sort_values(by="transaction_date").reset_index(drop=True)

# # filters_display = st.button("Show Filters")
# # region_select = alt.selection_single(fields=["region"], empty="all")
# # st.session_state.filter_region = None

# # if filters_display:
# #     try:
# #         region_filter = ['All']
# #         region_filter.extend(regions)
# #         st.write(f"regions: {region_filter}")
# #         selected_region = st.selectbox("Select Region", region_filter)
# #     finally:
# #         if selected_region != "All":
# #             st.session_state.filter_region = selected_region

# # if st.session_state.filter_region != None:
# #     sales_data = sales_data[sales_data["region"] == selected_region]
# filter_toggle = st.toggle("Show Filters", value=st.session_state.toggle, key=st.session_state["toggle_key"])
# region_select = alt.selection_single(fields=["region"], empty="all")

# if filter_toggle:
#     col1, col2 = st.columns(2)
#     with col1:
#         region_options = ["All"] + regions
#         filter_region = st.selectbox("Drop Down Filter", region_options)
#         if filter_region != "All":
#             sales_data = sales_data[sales_data["region"] == filter_region]
#         region_options = ["All"] + regions
        
#     with col2:
#         transaction_range = st.slider("Temporal Filter", 0, 250000, (0, 250000))
#         sales_data = sales_data[(sales_data["transaction_amount"]>=transaction_range[0]) & (sales_data["transaction_amount"]<=transaction_range[1])]
#     gender_filter = st.segmented_control("Gender Filter", ["All", "Male", "Female", "Unknown"])

#     st.session_state.toggle_save = False
#     save_toggle = st.toggle("Save Filtered Data", value =st.session_state.toggle_save)
#     if save_toggle:
#         col1, col2 = st.columns(2)
#         with col1:
#             save_title = st.text_input("Save Title")
#         with col2:
#             save_button = st.button("Save", on_click=save_feature)
        
            

    #time_filter = st.slider("Select Time Range", 0, 12, (0, 12))
    #sales_data = sales_data[sales_data["transaction_date"].apply(lambda x: x in months[time_filter[0]:time_filter[1]])]

# region_filter = ["All"]
# region_filter.extend(regions)
# selected_region = st.selectbox("Select Region", region_filter)
# if selected_region != "All":
#     sales_data = sales_data[sales_data["region"] == selected_region]

# region_pie = (
#     (
#         alt.Chart(sales_data)
#         .mark_arc(innerRadius=50)
#         .encode(
#             theta=alt.Theta(
#                 "transaction_amount",
#                 type="quantitative",
#                 aggregate="sum",
#                 title="Sum of Transactions",
#             ),
#             color=alt.Color(
#                 field="region",
#                 type="nominal",
#                 scale=alt.Scale(domain=regions, range=colors),
#                 title="Region",
#             ),
#             opacity=alt.condition(region_select, alt.value(1), alt.value(0.25)),
#         )
#     )
#     .add_selection(region_select)
#     .properties(title="Region Sales")
# )

# region_summary = (
#     (
#         alt.Chart(sales_data)
#         .mark_bar()
#         .encode(
#             x=alt.X(
#                 "month(transaction_date)",
#                 type="temporal",
#             ),
#             y=alt.Y(
#                 field="transaction_amount",
#                 type="quantitative",
#                 aggregate="sum",
#                 title="Total Sales",
#             ),
#             color=alt.Color(
#                 "region",
#                 type="nominal",
#                 title="Regions",
#                 scale=alt.Scale(domain=regions, range=colors),
#                 legend=alt.Legend(
#                     direction="vertical",
#                     symbolType="triangle-left",
#                     tickCount=4,
#                 ),
#             ),
#         )
#     )
#     .transform_filter(region_select)
#     .properties(width=700, title="Monthly Sales")
# )

# sellers_monthly_pie = (
#     (
#         alt.Chart(sales_data)
#         .mark_arc(innerRadius=10)
#         .encode(
#             theta=alt.Theta(
#                 field="transaction_amount",
#                 type="quantitative",
#                 aggregate="sum",
#                 title="Total Transactions",
#             ),
#             color=alt.Color(
#                 "month(transaction_date)",
#                 type="temporal",
#                 title="Month",
#                 scale=alt.Scale(domain=months, range=colors),
#                 legend=alt.Legend(
#                     direction="vertical",
#                     symbolType="triangle-left",
#                     tickCount=12,
#                 ),
#             ),
#             facet=alt.Facet(
#                 field="seller",
#                 type="nominal",
#                 columns=8,
#                 title="Sellers",
#             ),
#             tooltip=alt.Tooltip(["sum(transaction_amount)", "month(transaction_date)"]),
#         )
#     )
#     .transform_filter(region_select)
#     .properties(width=150, height=150, title="Sellers transactions per month")
# )




# top_row = region_pie | region_summary
# full_chart = top_row & sellers_monthly_pie
# st.altair_chart(full_chart)





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
