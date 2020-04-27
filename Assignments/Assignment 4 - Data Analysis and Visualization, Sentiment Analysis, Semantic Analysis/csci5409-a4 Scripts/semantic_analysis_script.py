import json
import math
import re
import csv


def create_vectors():
    print("Loading cleaned_news.json...")
    with open('cleaned_news.json', 'r') as read_file:
        data = json.load(read_file)
    print("Creating vectors...")
    article_count = 0
    for i in data:
        articles[article_count] = {}
        articles[article_count]['bag_of_words'] = []
        articles[article_count]['canada_freq'] = 0
        for j in i:
            articles[article_count]['bag_of_words'] += re.findall(r"\b\w+-?\w+\b", i[j])

        articles[article_count]['text'] = " ".join(k for k in articles[article_count]['bag_of_words'])
        for word in search_vector_dict.keys():
            word_count = len(re.findall(rf"{word}", articles[article_count]['text']))
            if word_count > 0:
                search_vector_dict[word] += 1
            if word == 'canada':
                articles[article_count]['canada_freq'] += word_count

        article_count += 1
    print("Vectors successfully created.")


def compute_tfidf():
    print("Computing TF-IDF...")
    metadata = ('Search Query', 'Document containing term (df)', 'Total Documents(N)/ number of documents term '
                                                                 'appeared (df)', 'Log10 (N/df)')
    N = len(articles)
    with open('TF-IDF.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['Total Documents', str(N)])
        writer.writerow(metadata)
        for i in search_vector_dict:
            writer.writerow([i, search_vector_dict[i], str(str(N) + "/" + str(search_vector_dict[i])),
                             str(round(math.log10(N / search_vector_dict[i]), 2))])
    print("Data successfully stored in TF-IDF.csv")


def compute_canada_freq_distribution():
    print("Computing frequency distribution of the word 'Canada'...")
    metadata = (
        'Canada appeared in ' + str(search_vector_dict['canada']) + ' documents', 'Total Words (m)', 'Frequency (f)')
    with open('canada-frequency-distribution.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['Term', 'Canada'])
        writer.writerow(metadata)
        article_count = 1
        for i in articles:
            if articles[i]['canada_freq'] > 0:
                m = len(articles[i]['bag_of_words'])
                f = articles[i]['canada_freq']
                relative_frequency = f / m
                if relative_frequency > hrf_article['hrf']:
                    hrf_article['hrf'] = relative_frequency
                    hrf_article['article'] = articles[i]
                writer.writerow(['Article #' + str(article_count), str(m), str(f)])
                article_count += 1
    print("Data successfully stored in canada-frequency-distribution.csv")


articles = {}
hrf_article = {'hrf': 0.0}
search_vector = ['Canada', 'University', 'Dalhousie University', 'Halifax', 'Business']
search_vector_dict = {}

for i in search_vector:
    search_vector_dict[i.lower()] = 0

create_vectors()
compute_tfidf()
compute_canada_freq_distribution()
print("\n\nThe news article with the highest relative frequency is:")
print(hrf_article['article']['text'])
print("Relative Frequency: " + str(hrf_article['hrf']))
