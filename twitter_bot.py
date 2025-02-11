import os
import json
import tweepy 
import schedule 
import requests
import time 
from dotenv import load_dotenv

# Load API keys from .env file 
load_dotenv()

# Twitter API credentials 
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

# Deepseek API keys from openrouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

#Authenticate with X-API
auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Generate tweet using deepseek 
def generate_tweet():
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free",
                "messages": [{"role": "user", "content": "Generate an insightful tweet about personal development."}]
            })
        )

        if response.status_code == 200:
            ai_response = response.json()
            tweet_content = ai_response.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            return tweet_content if tweet_content else "AI tweet generation failed."
        else:
            print(f"Error: API returned status {response.status_code}")
            return "Error: Unable to generate tweet."

    except Exception as e:
        print(f"DeepSeek API error: {e}")
        return "Error: AI generation failed."

#Function to post a tweet 
def post_tweet():
    tweet = generate_tweet()
    try:
        api.update_status(tweet)
        print(f"Tweet posted:{tweet}")
    except Exception as e:
        print(f"Error: {e}")


# Schedule tweet (Every 1 hours)
schedule.every(1).hours.do(post_tweet)

#Automating the bot 
if __name__ == "__main__":
    print("AutoTweet Ai is running.....")
    while True:
        schedule.run_pending()
        time.sleep(60)