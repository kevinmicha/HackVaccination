# Import necessary libraries
import time
import asyncio
import random
import pandas as pd
from typing import Any, Dict, List

from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

# Data Models
class PostRequest(Model):
    text: str

class PostResponse(Model):
    timestamp: int
    text: str
    agent_address: str

class ImageRequest(Model):
    prompt: str


class ImageResponse(Model):
    url: str

class SentimentRequest(Model):
    text: str

class SentimentResponse(Model):
    response: str

class WebSearchRequest(Model):
    query: str

class WebSearchResult(Model):
    title: str
    url: str
    content: str

class WebSearchResponse(Model):
    query: str
    results: List[WebSearchResult]

class ContextPrompt(Model):
    context: str
    text: str

class Response(Model):
    text: str

# Mailbox Agent Setup
AGENT_MAILBOX_KEY = "302e95ba-99cd-4aa3-bef0-01ff4b4aea1c"
agent = Agent(name="RestAPPI", seed="myth-buster-app-seeding-kmmm", port=8001,
              mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai")

fund_agent_if_low(agent.wallet.address())

# External Agent Addresses
SENTIMENT_AGENT_ADDRESS = "agent1qvzs7zhwdcx6rlnyzs9p9sjjq4zscd44zvx8fnpflrlu2ptvlh5fxlkwzge"
OPENAI_AGENT_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"
TAVILY_AGENT_ADDRESS = "agent1qt5uffgp0l3h9mqed8zh8vy5vs374jl2f8y0mjjvqm44axqseejqzmzx9v8"
AI_IMAGE_ADDRESS = "agent1qwvw7n7vn0ze4c0eq3q7wsjs6luv85mmmd8kw2m0ncuk2j3cnqlkk32kp9y"


pending_responses = {}

# Variable to store the generated negative tweet
negative_tweet = ""

async def await_response() -> Any:
    correlation_id = str(int(time.time()))  # Unique correlation ID
    event = asyncio.Event()
    pending_responses[correlation_id] = {"event": event, "response": None}
    await event.wait()
    return correlation_id, pending_responses.pop(correlation_id)["response"]

# Startup Event: Generate a Single Negative Tweet and Trigger Workflow
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(agent.address)
    global negative_tweet
    ctx.logger.info("Agent started.")

    # Load and process the CSV file
    csv_file_path = "df_simulated_tweets_2h.csv"  # Adjust path as needed
    try:
        tweets_df = pd.read_csv(csv_file_path)
    except Exception as e:
        ctx.logger.error(f"Failed to load CSV file: {e}")
        return

    # Filter for negative sentiment tweets
    negative_tweets = tweets_df[tweets_df["Sentiment"] == "Negative"]

    # Calculate weight based on engagement
    negative_tweets["Weight"] = (
        negative_tweets["Retweets"] + negative_tweets["Likes"] + negative_tweets["Comments"]
    )

    # Extract keywords from the top five most impactful tweets
    top_five_tweets = negative_tweets.sort_values(by="Weight", ascending=False).head(5)
    all_keywords = []
    for keywords in top_five_tweets["Keywords"]:
        all_keywords.extend(keywords.split(", "))
    random.shuffle(all_keywords)  # Shuffle to ensure variability

    # Generate a unique tweet using keywords
    keywords_section = ", ".join(all_keywords[:10])  # Use the top 10 shuffled keywords
    weighted_metrics = (
        f"{top_five_tweets['Retweets'].sum()} retweets, "
        f"{top_five_tweets['Likes'].sum()} likes, "
        f"{top_five_tweets['Comments'].sum()} comments"
    )
    negative_tweet = (
        f"Vaccines are dangerous! Why isn't anyone talking about {keywords_section}? "
        f"Too many side effects, no transparency, and rushed trials. "
        f"#QuestionEverything"
    )

    ctx.logger.info(f"Generated single negative tweet: {negative_tweet}")

    # Send the generated tweet to the sentiment analysis pipeline
    await ctx.send(SENTIMENT_AGENT_ADDRESS, SentimentRequest(text=negative_tweet))


@agent.on_message(model=SentimentResponse)
async def handle_sentiment_response(ctx: Context, sender: str, msg: SentimentResponse):
    """Handle sentiment analysis responses."""
    ctx.logger.info(f"Received sentiment analysis response: {msg.response}")

    if msg.response == "NEGATIVE":  # Correctly using msg.response
        # Send web search request to Tavily agent
        web_search_request_text = f"Help me find relevant documents to debunk: {negative_tweet}"
        await ctx.send(TAVILY_AGENT_ADDRESS, WebSearchRequest(query=web_search_request_text))


@agent.on_message(model=WebSearchResponse)
async def handle_web_search_response(ctx: Context, sender: str, msg: WebSearchResponse):
    """Handle web search responses."""
    ctx.logger.info("Received web search response from Tavily agent.")

    response_summary = [
        f"Title: {result.title}\nURL: {result.url}\nContent: {result.content}"
        for result in msg.results
    ]
    response_text = "\n\n".join(response_summary)

    # Prepare OpenAI prompt to create a post referencing the previously generated tweet
    openai_prompt = ContextPrompt(
        context=f"Below are relevant documents debunking the myth:\n{response_text}",
        text=(
            f"Create a social media post to go against the following tweet:\n\n'{negative_tweet}'\n\n"
            f"Use the provided information to educate people and debunk the claims made in this tweet."
        )
    )

    # Send prompt to OpenAI agent
    await ctx.send(OPENAI_AGENT_ADDRESS, openai_prompt)


@agent.on_message(model=Response)
async def handle_openai_response(ctx: Context, sender: str, msg: Response):
    """Handle the response from the OpenAI agent."""
    ctx.logger.info(f"Received post creation response: {msg.text}")
    prompt = ImageRequest(
        prompt="In the background, a bright rainbow arches across a clear blue sky, each color representing different forms of support and love. A gentle breeze carries the sweet fragrance of blooming flowers, evoking a sense of peace and connection. This scene embodies the idea that the right care and nurturing, represented by the gardener and the vibrant plants, lead to a flourishing community. The message reads: Together, we cultivate a healthier tomorrow. Let this imagery reflect trust and unity in the quest for well-being, while subtly hinting at the protective role of vaccination in nurturing a vibrant, thriving garden of life."
    )
    
    await ctx.send(AI_IMAGE_ADDRESS, prompt)

@agent.on_message(ImageResponse)
async def handle_response(ctx: Context, sender: str, msg: ImageResponse):
    ctx.logger.info(f"Received response from {sender}: {msg.url}")


if __name__ == "__main__":
    agent.run()
