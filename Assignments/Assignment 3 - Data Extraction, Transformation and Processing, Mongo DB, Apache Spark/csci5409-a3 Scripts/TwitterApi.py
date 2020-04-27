import tweepy
import json
import re


class TwitterApi:

    def __init__(self):
        self.api = None

    def authentication(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)

    def fetch_tweets(self, search_keywords, file_name):
        print("Fetching tweets...")
        tweets = []
        self.authentication()
        for keyword in search_keywords:
            for page in tweepy.Cursor(self.api.search, q=keyword, lang="en", tweet_mode="extended").pages(50):
                for i in page:
                    tweets.append(i._json)
        print("Fetching completed.")
        with open(file_name, 'w') as jsonFile:
            json.dump(tweets, jsonFile, indent=4)
        print("Tweets stored into ", file_name)
        return tweets

    def clean_tweets(self, source_file_name, destination_file_name):
        print("Loading JSON file...")
        with open(source_file_name, 'r') as read_file:
            data = json.load(read_file)
        tweets = []
        print("Cleaning tweets...")
        for i in data:
            filtered_tweet = {'name': ''.join([c for c in i.get('user').get('name') if ord(c) < 128]),
                              'screen_name': ''.join([c for c in i.get('user').get('screen_name') if ord(c) < 128]),
                              'location': ''.join([c for c in i.get('user').get('location') if ord(c) < 128]),
                              'created_at': ''.join([c for c in i.get('user').get('created_at') if ord(c) < 128])}
            if i.get('retweeted_status'):
                tweet = i.get('retweeted_status').get('full_text')
            else:
                tweet = i.get('full_text')

            tweet = ''.join([c for c in tweet if ord(c) < 128])
            tweet = re.sub(r"http\S+", "", tweet)
            tweet = re.sub(r"\n", " ", tweet)
            tweet = re.sub(r"@\w*", " ", tweet)
            tweet = re.sub(r"^(RT|FAV)", " ", tweet)
            tweet = re.sub(r"[^\w\s]", "", tweet)
            tweet = tweet.strip()
            tweet = re.sub(r"#\w*", " ", tweet.lower())

            filtered_tweet['full_text'] = tweet
            tweets.append(filtered_tweet)

        print("Cleaning completed.")
        with open(destination_file_name, 'w') as jsonFile:
            json.dump(tweets, jsonFile, indent=4)
        print("Cleaned tweets stored into ", destination_file_name)
        return tweets


# Twitter application API
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""
searchKeywords = ["Canada Education", "Canada", "University", "Dalhousie University", "Halifax"]
twitterObj = TwitterApi()
twitter_data = twitterObj.fetch_tweets(searchKeywords, 'tweets.json')
twitterObj.clean_tweets('tweets.json', 'cleaned_tweets.json')


