import streamlit as st
import requests
import asyncio
import threading
import pandas as pd

def send_post_request(text):
    url = "http://localhost:8001/rest/post"
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

st.set_page_config(page_title="Agent Interaction Dashboard", layout="wide")

st.title("📊 Agent Interaction Dashboard by PCE and KM")
st.subheader("Interact with the system for sentiment analysis and myth-busting tasks.")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.header("🚀 Send a Post Request")
    post_text = st.text_area("Enter text:", height=150, placeholder="Type something...")
    if st.button("Submit", type="primary"):
        if post_text.strip():
            with st.spinner("Processing..."):
                try:
                    response = send_post_request(post_text)
                    st.success("Response Received")
                    response_df = pd.DataFrame.from_dict(response, orient="index", columns=["Value"])
                    st.table(response_df)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter some text.")

with col2:
    st.header("📋 Real-time Logs")
    log_display = st.container()
    log_data = []

    def add_log_entry(entry):
        log_data.append(entry)
        if len(log_data) > 10:
            log_data.pop(0)

    async def update_logs():
        while True:
            if log_data:
                with log_display:
                    st.write(
                        f"<div style='padding:10px;background-color:#f1f1f1;border-radius:5px;'>"
                        + "<br>".join(f"<b>•</b> {log}" for log in log_data)
                        + "</div>",
                        unsafe_allow_html=True,
                    )
            await asyncio.sleep(0.5)

    def run_async_log_thread():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(update_logs())

    threading.Thread(target=run_async_log_thread, daemon=True).start()

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
