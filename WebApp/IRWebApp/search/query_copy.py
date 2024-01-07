from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .wordtools import process_string
from heapq import nlargest
import pandas as pd


def search(query):
    query = process_string(query)
    df = pd.read_csv('testdata.csv', delimiter=',', header='infer', encoding='utf-8')
    speeches = df['processed_speeches'].tolist()
    speeches.append(query)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(speeches)

    ddsim_matrix = cosine_similarity(tfidf_matrix[len(speeches)-1,:], tfidf_matrix)

    similar = {}
    for i in range(len(speeches)-1):
        if ddsim_matrix[0,i] > 0:
            similar[i] = ddsim_matrix[0,i]    

    k = 80
    top_k_items = nlargest(k, similar.items(), key=lambda x: x[1])
    indices = []
    for item in top_k_items:
        indices.append(item[0])
    
    return indices   #df.iloc[indices].to_dict()

def search2(query, speeches):
    query = process_string(query)
    #df = pd.read_csv('testdata.csv', delimiter=',', header='infer', encoding='utf-8')
    #speeches = df['processed_speeches'].tolist()
    #list(speeches)
    speeches.append(query)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(speeches)

    ddsim_matrix = cosine_similarity(tfidf_matrix[len(speeches)-1,:], tfidf_matrix)

    similar = {}
    for i in range(len(speeches)-1):
        if ddsim_matrix[0,i] > 0:
            similar[i] = ddsim_matrix[0,i]    

    k = 80
    top_k_items = nlargest(k, similar.items(), key=lambda x: x[1])
    indices = []
    for item in top_k_items:
        indices.append(item[0])
    
    return indices

def mod_query(query):
    return process_string(query)