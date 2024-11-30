#Import necessary libraries
import time
import asyncio
from typing import Any, Dict, List

from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low


#Data Models for Post Request
class PostRequest(Model):
    text: str
class PostResponse(Model):
    timestamp: int
    text: str
    agent_address: str



#Data Models for Sentiment Analyser Agent
class SentimentRequest(Model):
    text: str
class SentimentResponse(Model):
    response: str



#Data Models for Tavily Search Agent
class WebSearchRequest(Model):
    query: str
class WebSearchResult(Model):
    title: str
    url: str
    content: str
class WebSearchResponse(Model):
    query: str
    results: List[WebSearchResult]

#Data Model for OpenAI Agent
class ContextPrompt(Model):
    context: str
    text: str
class Response(Model):
    text: str



#Deifining and connecting Agent to Agentverse via Mailbox

#To get the AGENT_MAILBOX_KEY first leave the AGENT_MAILBOX_KEY empty and run the agent it will throw an error, copy the agent's address and go to Agentverse switch to Local Agent and then Connect Agent paste your agent address here and copy the generated mailbox key
AGENT_MAILBOX_KEY = "49d02d1b-0aed-4321-83fb-ad13e1c530b5"
agent = Agent(name="Rest API", seed="myth-buster-app-seedingkm", port=8001,
              mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai")

#Add testnet funds to the agent's wallet for it to register on the network
fund_agent_if_low(agent.wallet.address())

#Define Agent Address
SENTIMENT_AGENT_ADDRESS = "agent1qvzs7zhwdcx6rlnyzs9p9sjjq4zscd44zvx8fnpflrlu2ptvlh5fxlkwzge"
OPENAI_AGENT_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"
TAVILY_AGENT_ADDRESS = "agent1qt5uffgp0l3h9mqed8zh8vy5vs374jl2f8y0mjjvqm44axqseejqzmzx9v8"

# To track responses for POST requests
pending_responses = {}

async def await_response() -> Any:
    """
    Utility function to handle asyncio.Event logic.
    Generates a unique correlation ID and waits for a response.
    """
    correlation_id = str(int(time.time()))  # Unique correlation ID
    event = asyncio.Event()
    pending_responses[correlation_id] = {"event": event, "response": None}
    await event.wait()
    return correlation_id, pending_responses.pop(correlation_id)["response"]

#Print Agent address on startup
@agent.on_event('startup')
async def startup(ctx: Context):
    ctx.logger.info(agent.address)


@agent.on_rest_post("/rest/post", PostRequest, PostResponse)
async def handle_post(ctx: Context, req: PostRequest) -> PostResponse:
    ctx.logger.info(f"Received POST request: {req.text}")

    # Send sentiment analysis request
    ctx.logger.info(f"Sending message to Sentiment Analyser agent with data: {req.text}")
    await ctx.send(SENTIMENT_AGENT_ADDRESS, SentimentRequest(text=req.text))

    _, sentiment_response_data = await await_response()
    ctx.logger.info(f"Sentiment response: {sentiment_response_data}")


    #If the tweet is negative, search the web to find relevant information to overcome this misconception and create a positive social media post
    if sentiment_response_data == "NEGATIVE":
        # Send web search request to Tavily agent
        ctx.logger.info(f"Sending message to Tavily agent with data: {req.text}")
        tavily_request_text = f"Help me find relevant documents to overcome the following myth: {req.text}"
        await ctx.send(TAVILY_AGENT_ADDRESS, WebSearchRequest(query=tavily_request_text))

        _, tavily_response_data = await await_response()
        ctx.logger.info(f"Tavily response: {tavily_response_data}")

        # Prepare prompt for OpenAI agent
        prompt = ContextPrompt(
            context=f"Below are the relevant documents debunking the myth:\n{tavily_response_data}",
            text=f"Create a social media post to educate people and debunk the myth: {req.text}. Use the information and links provided.",
        )

        # Send OpenAI request
        ctx.logger.info(f"Sending prompt to OpenAI agent: {prompt.text}")
        await ctx.send(OPENAI_AGENT_ADDRESS, prompt)

        _, openai_response_data = await await_response()
        ctx.logger.info(f"OpenAI response: {openai_response_data}")

        # Return the response
        return PostResponse(
            text=openai_response_data,
            agent_address=ctx.agent.address,
            timestamp=int(time.time()),
        )
    else:
        return PostResponse(
            text="POSITIVE Tweet",
            agent_address=ctx.agent.address,
            timestamp=int(time.time()),
        )


@agent.on_message(model=SentimentResponse)
async def handle_sentiment_response(ctx: Context, sender: str, msg: SentimentResponse):
    """Handle the response message from the Sentiment Analyser agent."""
    ctx.logger.info(f"Received response from Sentiment Analyser agent: {msg.response}")
    for correlation_id, data in pending_responses.items():
        if data["response"] is None:
            data["response"] = msg.response
            data["event"].set()
            break



@agent.on_message(model=WebSearchResponse)
async def handle_web_search_response(ctx: Context, sender: str, msg: WebSearchResponse):
    """Handle the response message from Tavily agent."""
    ctx.logger.info(f"Received response from Tavily agent: {sender}")
    response_summary = [
        f"Title: {result.title}\nURL: {result.url}\nContent: {result.content}"
        for result in msg.results
    ]
    response_text = "\n\n".join(response_summary)

    for correlation_id, data in pending_responses.items():
        if data["response"] is None:
            data["response"] = response_text
            data["event"].set()
            break


@agent.on_message(model=Response)
async def handle_openai_response(ctx: Context, sender: str, msg: Response):
    """Handle the response message from the OpenAI agent."""
    ctx.logger.info(f"Received response from OpenAI agent: {msg.text}")
    for correlation_id, data in pending_responses.items():
        if data["response"] is None:
            data["response"] = msg.text
            data["event"].set()
            break


if __name__ == "__main__":
    agent.run()