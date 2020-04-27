from newsapi import NewsApiClient
import requests
import json
import re


class NewsApi:

    def fetch_news(self, search_keywords):
        print("Fetching news...")
        news = []
        news_api = NewsApiClient(api_key)
        for keyword in search_keywords:
            url = ('http://newsapi.org/v2/everything?'
                   'q=' + keyword + '&'
                                    'sortBy=popularity&'
                                    'apiKey=' + api_key)
            response = requests.get(url).json()
            # print(response)
            arr = response['articles']
            for i in arr:
                if i['content']:
                    temp = {'title': i.get('title'), 'description': i.get('description'), 'content': i.get('content')}
                else:
                    temp = {'title': i.get('title'), 'description': i.get('description'), 'content': "None"}
                news.append(temp)

        print("Fetching completed")

        print("Storing the news articles in the json file...")
        with open('news.json', 'w') as jsonFile:
            json.dump(news, jsonFile, indent=4)
        print("Successfully stored.")
        return news

    def clean_news(self, source_file_name, destination_file_name):
        print("Loading JSON file...")
        with open(source_file_name, 'r') as read_file:
            data = json.load(read_file)
        news = []
        print("Cleaning news articles...")
        for i in data:
            filtered_news = {}
            for j in i:
                cle = ''.join([c for c in i[j] if ord(c) < 128])
                cle = re.sub(r"\n|\r", " ", cle)
                cle = re.sub(r"@\w*", " ", cle)
                cle = re.sub(r"[^\w\s]", "", cle.lower())
                cle = cle.strip()
                filtered_news[j] = cle

            news.append(filtered_news)

        print("Cleaning completed.")
        with open(destination_file_name, 'w') as jsonFile:
            json.dump(news, jsonFile, indent=4)
        print("Cleaned news articles stored into ", destination_file_name)
        return news


# NewsAPI
api_key = ''
searchKeywords = ["Canada Education", "Canada", "University", "Dalhousie University", "Halifax", "Toronto", "Moncton"]
newsObj = NewsApi()
newsObj.fetch_news(searchKeywords)
newsObj.clean_news('news.json', 'cleaned_news.json')
