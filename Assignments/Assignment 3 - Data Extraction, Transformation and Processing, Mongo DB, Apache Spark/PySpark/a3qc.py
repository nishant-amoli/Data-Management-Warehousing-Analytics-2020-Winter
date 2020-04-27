import json
import pymongo
import json


class a3qc:
    def create_text_file(self):
        with open('cleaned_tweets.json', 'r') as read_file:
            data_tweets = json.load(read_file)

        with open('cleaned_news.json', 'r') as read_file:
            data_news = json.load(read_file)

        with open('tweets_and_articles.txt', 'w') as read_file:
            for i in data_tweets:
                for j in i['full_text']:
                    if j != "\n":
                        read_file.write(j.lower())

    def extract_movie_ratings(self):
        user = 'nishant'
        passwordPhrase = 'vision'
        ip = '18.219.84.33'
        database = 'csci5408a3'
        connection = pymongo.MongoClient("mongodb://" + user + ":" + passwordPhrase + "@" + ip + "/" + database)
        db = connection[database]
        collection = db['movies']
        movies_data = collection.find({}, {'title': 1, 'ratings': 1, 'genre': 1, 'plot': 1, '_id': 0})
        for movie in movies_data:
            print(movie)
        print(" The collection contains a total of ", collection.estimated_document_count(), " documents.")


obj = a3qc()
obj.create_text_file()
obj.extract_movie_ratings()
