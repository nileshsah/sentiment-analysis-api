import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
import json
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from pprint import pprint
import summarize

# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def solve(file_data):
    data = file_data

    #not super pythonic, no, not at all.
    #use extend so it's a big flat list of vocab
    totalvocab_stemmed = []
    totalvocab_tokenized = []
    review_content = []
    for review in data['Reviews']:
        i = review['Content']
        review_content.append(i)
        allwords_stemmed = tokenize_and_stem(i) #for each item in 'synopses', tokenize/stem
        totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
        
        allwords_tokenized = tokenize_only(i)
        totalvocab_tokenized.extend(allwords_tokenized)


    vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
    print 'there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame'

    #define vectorizer parameters
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                     min_df=0.2, stop_words='english',
                                     use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

    tfidf_matrix = tfidf_vectorizer.fit_transform(review_content) #fit the vectorizer to synopses

    print(tfidf_matrix.shape)

    terms = tfidf_vectorizer.get_feature_names()

    print (terms)

    dist = 1 - cosine_similarity(tfidf_matrix)

    num_clusters = 5
    km = KMeans(n_clusters=num_clusters)
    km.fit(tfidf_matrix)

    clusters = km.labels_.tolist()

    print (clusters)

    groups = {}

    for i in range(len(clusters)):
      if clusters[i] not in groups.keys():
        groups[ clusters[i] ] = []
      groups[ clusters[i] ].append(review_content[i])


    d3 = {}
    d3["name"] = data['Product']
    d3["children"] = []

    for idx in groups:
      parent  = {}
      parent["name"] = summarize.getSummarizedText( "".join( groups[idx] )).replace('\n','')
      parent["children"] = []
      
      for content in groups[idx]:
        child = {}
        child["name"] = content
        
        parent["children"].append(child)
      
      d3["children"].append(parent)

    return (json.dumps(d3))
