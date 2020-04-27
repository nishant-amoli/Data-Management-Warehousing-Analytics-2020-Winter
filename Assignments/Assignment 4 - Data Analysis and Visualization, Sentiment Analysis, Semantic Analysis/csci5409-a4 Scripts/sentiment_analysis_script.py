import json
import re
import csv


def create_bag_of_words():
    print("Loading JSON file...")
    with open('cleaned_tweets.json', 'r') as read_file:
        data = json.load(read_file)
    print("Creating bag of words...")
    tweetCount = 0
    for i in data:
        tweets[tweetCount] = {}
        tweets[tweetCount]['tweet'] = i['full_text']
        tweets[tweetCount]['bagOfWords'] = {}
        words = re.findall(r"\b\w+-?\w+\b", i['full_text'])

        for word in words:
            if word not in tweets[tweetCount]['bagOfWords']:
                tweets[tweetCount]['bagOfWords'][word] = 1
            else:
                tweets[tweetCount]['bagOfWords'][word] += 1
        tweetCount += 1
    print("Bags of words successfully created.")


def create_sentiment_vectors():
    global positive_opinion_vector
    global negative_opinion_vector
    print("Loading positive-words.txt...")
    with open('positive-words.txt', 'r') as read_file:
        positive_opinion_vector = read_file.read().splitlines()

    print("Loading negative-words.txt...")
    with open('negative-words.txt', 'r') as read_file:
        negative_opinion_vector = read_file.read().splitlines()

    print("Opinion vectors successfully created.")


def analyze_sentiments():
    global positive_opinion_vector
    global negative_opinion_vector
    metadata = ('S.No', 'Message/Tweet', 'Match', 'Polarity')
    print("Performing sentiment analysis...")
    with open('tagged-tweets.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(metadata)
        for t in tweets:
            row = [t, tweets[t]['tweet']]

            positive = list(set(positive_opinion_vector) & set(list(tweets[t]['bagOfWords'].keys())))
            negative = list(set(negative_opinion_vector) & set(list(tweets[t]['bagOfWords'].keys())))
            positiveMagnitude = 0
            negativeMagnitude = 0
            for i in positive:
                positiveMagnitude += tweets[t]['bagOfWords'][i]
            for i in negative:
                negativeMagnitude += tweets[t]['bagOfWords'][i]

            match = " ".join(j for j in positive)
            temp = " ".join(j for j in negative)
            match = match + " " + temp
            row.append(match)

            if positiveMagnitude > negativeMagnitude:
                row.append("positive")
            elif positiveMagnitude < negativeMagnitude:
                row.append("negative")
            else:
                row.append("neutral")

            writer.writerow(row)
    print("Tagged tweets successfully stored in tagged-tweets.csv")


tweets = {}
positive_opinion_vector = []
negative_opinion_vector = []
create_bag_of_words()
create_sentiment_vectors()
analyze_sentiments()