import omdb
import json
import re

import requests


class OmdbApi:
    def fetch_movies(self, search_keywords):
        print("Fetching movies...")
        movies = []
        omdb.set_default('apikey', api_key)
        for keyword in search_keywords:
            res = requests.get(url + keyword)
            encoded = json.dumps(res.json()['Search'])
            decoded = json.loads(encoded)
            for j in decoded:
                req = requests.get(url_ratings + j['Title'])
                movie = json.dumps(req.json())
                data = json.loads(movie)
                temp = {'title': data['Title'], 'year': data['Year'], 'genre': data['Genre'], 'type': data['Type'],
                        'plot': data['Plot']}
                movies.append(temp)

        print("Fetching completed")

        print("Storing the movie data in the json file...")
        with open('movies.json', 'w') as jsonFile:
            json.dump(movies, jsonFile, indent=4)
        print("Successfully stored.")

    def clean_movies(self, source_file_name, destination_file_name):
        print("Loading JSON file...")
        with open(source_file_name, 'r') as read_file:
            data = json.load(read_file)
        movies = []
        print("Cleaning movie data...")
        for i in data:
            filtered_movies = {}
            for j in i:
                cle = ''.join([c for c in i[j] if ord(c) < 128])
                cle = re.sub(r"[^\w\s]", "", cle.lower())
                cle = cle.strip()
                filtered_movies[j] = cle

            movies.append(filtered_movies)

        print("Cleaning completed.")
        with open(destination_file_name, 'w') as jsonFile:
            json.dump(movies, jsonFile, indent=4)
        print("Cleaned movie data stored into ", destination_file_name)
        return movies


api_key = ''
url = "http://www.omdbapi.com/?i=tt3896198&apikey=" + api_key + "&s="
url_ratings = "http://www.omdbapi.com/?i=tt3896198&apikey=" + api_key + "&t="
searchKeywords = ["Alberta", "Canada", "University", "Niagara", "Halifax", "Toronto", "Moncton", "Vancouver"]
moviesObj = OmdbApi()
moviesObj.fetch_movies(searchKeywords)
moviesObj.clean_movies('movies.json', 'cleaned_movies.json')
