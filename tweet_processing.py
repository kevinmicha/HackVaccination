import tweepy
import pandas as pd
import os
from dotenv import load_dotenv

# Load Twitter API credentials from .env
load_dotenv()
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

# Authenticate
auth = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_SECRET
)
api = tweepy.API(auth)

def fetch_tweets(query="vaccine", count=5):
    tweets = api.search_tweets(q=query, lang="en", count=count)
    data = [{"text": tweet.text, "created_at": tweet.created_at} for tweet in tweets]
    return pd.DataFrame(data)

def clean_tweet(tweet):
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'\@\w+|\#', '', tweet)
    tweet = re.sub(r"[^\w\s]", '', tweet)
    return tweet.lower()

def preprocess_tweets(file_path="tweets.csv"):
    df = pd.read_csv(file_path)
    df["cleaned_text"] = df["text"].apply(clean_tweet)
    return df

if __name__ == "__main__":
    df = preprocess_tweets()
    print(df.head())
    df.to_csv("cleaned_tweets.csv", index=False)
    df = fetch_tweets()
    print(df.head())
    df.to_csv("tweets.csv", index=False)
