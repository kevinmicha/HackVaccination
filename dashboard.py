import streamlit as st
import requests
import asyncio
import threading

def send_post_request(text):
    url = "http://localhost:8001/rest/post"
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def run_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Setup
st.title("Agent Interaction Dashboard by PCE and KM")

# Input area for sending a POST request
st.header("Send a Post Request")
post_text = st.text_area("Enter text for sentiment analysis and myth-busting:", height=100)
if st.button("Send Request"):
    if post_text.strip():
        with st.spinner("Processing your request..."):
            try:
                response = send_post_request(post_text)
                st.success("Request processed successfully!")
                st.json(response)
            except Exception as err:
                st.error(f"Failed to process the request: {err}")
    else:
        st.warning("Please enter some text before sending the request.")

# Not sure this will be useful
st.header("Real-time Logs")
log_container = st.empty()

log_queue = []

def append_log_entry(entry):
    log_queue.append(entry)

def display_logs():
    while True:
        if log_queue:
            log_container.text("\n".join(log_queue[-10:]))  # here we show last 10 entries from log
        asyncio.sleep(0.1)

log_thread = threading.Thread(target=display_logs, daemon=True)
log_thread.start()
