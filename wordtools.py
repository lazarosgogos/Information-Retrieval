# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 11:01:49 2023

@author: KoEle
"""

import string
import unicodedata as ud
import spacy
from greek_stemmer import stemmer

nlp = spacy.load("el_core_news_sm")

def preprocess_greek_strings(strings):
    # Define a translation table to remove punctuation
    greek_punctuation = ".,;:!?()[]{}<>-–—\"'«»…"
    translation_table = str.maketrans('', '', greek_punctuation)
    a = strings.translate(translation_table).lower()
    d = {ord('\N{COMBINING ACUTE ACCENT}'):None} 
    
    return ud.normalize('NFD',a).lower().translate(d)

def remove_words_from_string(input_string):
    # Split the input string into words
    words = input_string.split()

    # Remove words that are in the list of words to remove
    stopwords = createstopwordslist()
    filtered_words = [word for word in words if word not in stopwords]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

def createstopwordslist():
    stopwordsfile = open('stopwords1.txt', 'r')
    data = stopwordsfile.read()
    return data.replace('\n', ' ').split(" ")

def lematization(input_string):
    doc = nlp(input_string)
    intemediate = [token.lemma_ for token in doc]  
    return ' '.join(intemediate)

def stemming(input_string):
    words = input_string.split()
    for i, word in enumerate(words):
        words[i] = stemmer.stem_word(word, 'NNM')
    return ' '.join(words)

def remove_pun_word_stem(speeches):
    rows =[]
    for row in speeches:
        row = row.replace("ς","σ")
        row = preprocess_greek_strings(row)
        row = remove_words_from_string(row)
        row = stemming(row)
        rows.append(row)
        if len(rows)%10000 == 0:
            print(len(rows))
    return rows

def removepunctwordslem(dataset, lem = False, stem = True):
    rows = []
    for i,row in enumerate(dataset['speech']):
        row = preprocess_greek_strings(row)
        row = remove_words_from_string(row)
        if lem:
            row = lematization(row)
        if stem:
            row = stemming(row)
        if i%10000==0:
            print(i)
        #dataset.at[i,'speech'] = row
        rows.append(row)
    return rows

def removesmallspeechesindex(dataset, size):
    rows = []
    for row in dataset.index:
        if len(dataset.at[row, 'speech'])<size:
            rows.append(row)    
    return rows