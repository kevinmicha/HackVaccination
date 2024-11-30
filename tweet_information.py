import tweepy

# Authenticate with Twitter API
client = tweepy.Client(bearer_token="aaa")

# Define the query
query = '(vaccine OR "anti-vax" OR #VaccineHesitancy) -is:retweet lang:en'

# Fetch tweets
response = client.search_recent_tweets(query=query, max_results=1, 
                                       tweet_fields=['created_at', 'public_metrics', 'text', 'author_id'])

# Extract data
tweets = []
for tweet in response.data:
    tweets.append({
        "text": tweet.text,
        "created_at": tweet.created_at,
        "likes": tweet.public_metrics['like_count'],
        "retweets": tweet.public_metrics['retweet_count'],
        "author_id": tweet.author_id
    })

print(tweets)