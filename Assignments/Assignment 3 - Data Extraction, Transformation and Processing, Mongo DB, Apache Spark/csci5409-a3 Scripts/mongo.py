import pymongo
import json
from pymongo import MongoClient


class ExportToMongo:
    def __init__(self):
        self.connection = pymongo.MongoClient("mongodb://" + user + ":" + passwordPhrase + "@" + ip + "/" + database)
        self.db = self.connection[database]

    def __del__(self):
        self.connection.close()

    def export_tweets(self, collection):
        collection = self.db[collection]

        with open('cleaned_tweets.json', 'r') as read_file:
            data = json.load(read_file)

        print("Exporting tweets to remote mongodb...")

        for i in data:
            collection.insert_one(i)

        print(collection.estimated_document_count(), " documents successfully exported.")

    def export_news(self, collection):
        collection = self.db[collection]

        with open('cleaned_news.json', 'r') as read_file:
            data = json.load(read_file)

        print("Exporting news to remote mongodb...")

        for i in data:
            collection.insert_one(i)

        print(collection.estimated_document_count(), " documents successfully exported.")

    def export_movies(self, collection):
        collection = self.db[collection]

        with open('movies.json', 'r') as read_file:
            data = json.load(read_file)

        print("Exporting movie data to remote mongodb...")

        for i in data:
            collection.insert_one(i)

        print(collection.estimated_document_count(), " documents successfully exported.")


user = 'nishant'
passwordPhrase = 'vision'
ip = '18.219.84.33'
database = 'csci5408a3'
obj = ExportToMongo()
obj.export_tweets('tweets')
obj.export_news('news')
obj.export_movies('movies')
