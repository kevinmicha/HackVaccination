import streamlit as st

# Title of the dashboard
st.title("Response Dashboard")

# Layout the tweets in one row
st.subheader("Trigger Tweets")
col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://i.ibb.co/ZN7GnhN/Screenshot-from-2024-12-01-09-19-15.png", use_container_width=True)

with col2:
    st.image("https://i.ibb.co/XsTk9Kt/Screenshot-from-2024-12-01-09-17-58.png", use_container_width=True)

with col3:
    st.image("https://i.ibb.co/48xrJzD/image-antivax.png", use_container_width=True)

# Next row: Suggested tweet and sources side by side
st.subheader("Response")
col4, col5 = st.columns([2, 1])

with col4:
    st.subheader("Suggested Tweet")
    
    # Default suggested tweet text
    suggested_tweet = """Vaccines like the mRNA COVID-19 shots are *not* gene therapy. This claim misrepresents science. mRNA vaccines teach your cells to fight the virus without altering DNA. Millions have been safely protected. Learn more: [CDC](https://www.cdc.gov/coronavirus/2019-ncov/vaccines/different-vaccines/mrna.html)"""
    
    # Editable text area for the suggested tweet
    edited_tweet = st.text_area("Edit Suggested Tweet", value=suggested_tweet, height=150)

    # Add an image representing the main idea of the tweet
    st.image("https://i.ibb.co/4NjTRkL/vaccine-provax.webp", use_container_width=True)


    # Add a dummy "Post" button
    if st.button("Post"):
        st.success("Tweet posted successfully!")  # Dummy response

with col5:
    st.subheader("Sources")
    st.markdown("""
    - [World Health Organization (WHO): How Vaccines Work](https://www.who.int/news-room/feature-stories/detail/how-do-vaccines-work)
    - [CDC: Understanding mRNA COVID-19 Vaccines](https://www.cdc.gov/coronavirus/2019-ncov/vaccines/different-vaccines/mrna.html)
    - [Scientific Review: mRNA vaccines and their mechanism](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7749790/)
    - [Debunking DNA Modification Claims](https://www.factcheck.org/2021/03/scicheck-viral-video-uses-deceptive-editing-to-falsely-claim-mrna-vaccines-alter-dna/)
    - [Nature: How mRNA vaccines work](https://www.nature.com/articles/d41586-021-02483-w)
    - [FDA: Myths and Facts about COVID-19 Vaccines](https://www.fda.gov/consumers/consumer-updates/myths-and-facts-about-covid-19-vaccines)
    """)
