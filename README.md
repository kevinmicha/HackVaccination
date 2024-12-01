# HackVaccination
Addressing Vaccine Hesitancy through Social Media Analysis

Vaccine hesitancy is often fueled by misinformation propagated on social media platforms such as Twitter, Bluesky, and TikTok. This phenomenon affects diverse age groups and regions in varying ways, making it a multifaceted challenge. To address this issue, we propose a solution that enables Medical Affairs teams to intervene effectively and reduce reluctance toward vaccination.

Our approach involves leveraging Bluesky for data collection. We chose Bluesky because its platform allows easier scraping without requiring a lengthy developer signup process. The scraping functionality is implemented in the tweet_processing.py script, which dynamically retrieves the latest posts, including their text, reactions (likes, responses, and comments), timestamps, and location metadata.

As we expand this project, we aim to enhance our data collection by including posts in multiple languages. This will help us explore how misinformation spreads across linguistic and cultural boundaries. Additionally, we plan to gather more user-specific details, such as follower counts and demographic information, to better understand the influence and reach of individual users spreading misinformation.

Data Processing and Analysis

Once raw data is collected, we preprocess it using a Large Language Model (LLM). The LLM performs several key tasks:

Sentiment Analysis: Classifies posts as positive, negative, or neutral.
Keyword Extraction: Summarizes each post with three key terms.
Demographic Estimation: Estimates the gender and age group of the user.
Initially, we considered using Fetch.AI agents for processing. However, due to the high volume of real-time posts, the Fetch.AI query limits were quickly exceeded. To address this, we opted for an alternative agent that can handle the scale of data more efficiently.

Generating Insights and Interventions

Using the processed data, we compute actionable statistics to guide Medical Affairs interventions. Here’s how our system works, all of it is using agents from FetchAI.

Dynamic Triggering: Every fixed amount of time, our agent analyzes the latest processed data, identifying trends and generating prompts based on negative posts.
Validation: These prompts undergo additional sentiment analysis to confirm their negative tone using a sentiment analysis agent.
Counter-Misinformation Research: A trusted-source scraping agent (Tabily) identifies credible information to address the misinformation in the flagged posts.
Response Creation: An OpenAI agent generates draft posts for Medical Affairs to review and potentially publish, ensuring timely and effective communication.
Image Generation: Finally an Image generator agent creates an image to go with the post that we have created.

The repository also features a Streamlit app that provides an interactive dashboard to visualize and manage the insights generated by the system. The main page of the dashboard includes:

Time-Series Evolution: Tracks the trends of positive and negative posts over time.
Evolving Word Cloud: Displays key keywords weighted by importance and their evolution across time.
Geographic Insights: Maps the distribution of posts by geographic area.
Generated Posts: Lists posts created by the system, allowing users to click on each for detailed insights.
Clicking on a previously generated post opens a new tab that provides:

The original flagged post and the trusted sources used to counter misinformation.
The evolution of positive and negative posts following our intervention.
Reactions to the post, segmented by filters such as location, age group, or sentiment.
Alert System for Real-Time Response
The dashboard also includes an alert feature based on time-series trends. When an alert is triggered, a new tab is opened to display:

The event or trend that activated the alert.
A proposed response post created by the system's agents.
A button to review and publish the suggested post.
This dashboard streamlines real-time monitoring and facilitates rapid, informed interventions by Medical Affairs teams.

[![Python 3.8 - 3.11](https://img.shields.io/badge/Python-3.8%20--%203.11-blue)](https://www.python.org/downloads/release/python-3113/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/license/mit/)

### Manually handling the dependencies
If you want to use an existing environment, just omit the Anaconda commands above:
```bash
git clone https://github.com/kevinmicha/HACKVACCINATION
cd HACKVACCINATION
pip install .
```

or if you need to install it for your user only: 
```bash
python setup.py install --user 
```

## Requirements 

This project requires the following Python packages: 
* `uagents`
* `asyncio`
* `threading`
* `selenium`
* `webdriver_manager`
* `datetime`
* `csv`


    

