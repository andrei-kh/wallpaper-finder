import json
import praw
from PIL import Image
import requests


def load_credentials():
    with open('./.secret/credentials.json') as f:
        return json.load(f)


params = load_credentials()
reddit = praw.Reddit(client_id=params['client_id'],
                     client_secret=params['api_key'],
                     password=params['password'],
                     user_agent='Wallpaper finder:v0.0.1 (by /u/scoundreel)',
                     username=params['username'])

subreddit = reddit.subreddit('wallpaper')
for i, submission in enumerate(subreddit.top('month', limit=4)):
    url = submission.url
    im = Image.open(requests.get(url, stream=True).raw
    im.show()
