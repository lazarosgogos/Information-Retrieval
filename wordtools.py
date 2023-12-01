# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 11:01:49 2023

@author: KoEle
"""

import unicodedata as ud
from greek_stemmer import stemmer

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
    stopwordsfile = open('stopwords1-UTF8.txt', 'r')
    data = stopwordsfile.read()
    return data.replace('\n', ' ').split(" ")

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

def removesmallspeechesindex(dataset, size):
    rows = []
    for row in dataset.index:
        if len(dataset.at[row, 'speech'])<size:
            rows.append(row)    
    return rows

def process_string(query):
    query = query.replace("ς","σ")
    query = preprocess_greek_strings(query)
    query = remove_words_from_string(query)
    query = stemming(query)
    return query

# Τα ονόματα των παρατάξεων όπως αναφέρονται στη στήλη 'political_party'
political_parties = ['πανελληνιο σοσιαλιστικο κινημα', 
                     'νεα δημοκρατια',
                     'συνασπισμος της αριστερας των κινηματων και της οικολογιας',
                     'δημοκρατικη ανανεωση', 
                     'οικολογοι εναλλακτικοι (ομοσπονδια οικολογικων εναλλακτικων οργανωσεων)', 
                     'ανεξαρτητοι (εκτος κομματος)', 
                     'κομμουνιστικο κομμα ελλαδας',
                     'πολιτικη ανοιξη',
                     'δημοκρατικο κοινωνικο κινημα',
                     'συνασπισμος ριζοσπαστικης αριστερας',
                     'λαικος ορθοδοξος συναγερμος',
                     'δημοκρατικη αριστερα',
                     'ανεξαρτητοι ελληνες - πανος καμμενος',
                     'λαικος συνδεσμος - χρυση αυγη',
                     'ανεξαρτητοι δημοκρατικοι βουλευτες',
                     'το ποταμι',
                     'ανεξαρτητοι ελληνες εθνικη πατριωτικη δημοκρατικη συμμαχια',
                     'λαικη ενοτητα',
                     'δημοκρατικη συμπαραταξη (πανελληνιο σοσιαλιστικο κινημα - δημοκρατικη αριστερα)', 
                     'ενωση κεντρωων',
                     'κινημα αλλαγης',
                     'ελληνικη λυση - κυριακος βελοπουλος',
                     'μετωπο ευρωπαικης ρεαλιστικης ανυπακοης (μερα25)']

# Τα νέα διακριτά ονόματα των παρατάξεων
party_name_abbrev = ['ΠΑΣΟΚ',
                     'ΝΔ',
                     'ΣΥΝΑΣΠΙΣΜΟΣΣΥΡΙΖΑ',
                     'ΔΗΜΑΝΑΣΤΕΦΑΝΟΠΟΥΛΟΣ',
                     'ΟΙΚΕΝΑΛ',
                     'ΑΝΕΞΚΟΜ',
                     'ΚΚΕ',
                     'ΠΟΛΑΝ',
                     'ΔΗΚΚΙ',
                     'ΣΥΡΙΖΑ',
                     'ΛΑΟΣΚΑΡΑΤΖΑΦΕΡΗΣ',
                     'ΔΗΜΟΚΡΑΤΙΚ',# δε δουλεύει καλά το stemmer και μπορεί να υπάρχει conflict
                     'ΑΝΕΛ',
                     'ΧΡΑΥ',
                     'ΑΝΕΞΒΟΥΛΕ.',
                     'ΠΟΤΑΜ', # και εδώ υπάρχει conflict
                     'ΑΝΕΛ',
                     'ΛΑΙΚΕΝΟΤ',
                     'ΔΗΜΟΚΡΑΤΙΚ ΣΥΜΠΑΡΑΤΑΞ ΠΑΝΕΛΛΗΝΙ ΣΟΣΙΑΛΙΣΤΙΚ ΚΙΝΗΜ ΔΗΜΟΚΡΑΤΙΚ', # και εδώ
                     'ΕΝΚΕΝΤ',
                     'ΚΙΝΑΛ',
                     'ΕΛΛΥΣ',
                     'μερα25']

def change_party_names(dataframe): 
    """
    Μεθοδος για να εντοπίζει και να ενοποιεί τα ονόματα των παρατάξεων
    """
    # Λίστα των ονομάτων των πολιτικών παρατάξεων μετά από επεξεργσσία Stemming etc
    pros_party_names = []
    for party in political_parties:
        pros_party_names.append(process_string(party))

    # Αλλαγή του ονόματος κάποιων πολιτικών παρατάξεων για την εύρεση τους. πχ \
    # ΟΙΚΟΛΟΓ ΕΝΑΛΛΑΚΤΙΚ ΟΜΟΣΠΟΝΔΙ ΟΙΚΟΛΟΓΙΚ ΕΝΑΛΛΑΚΤΙΚ ΟΡΓΑΝΩΣΕ = ΟΙΚΟΛΟΓ ΕΝΑΛΛΑΚΤΙΚ 
    pros_party_names[4] = 'ΟΙΚΟΛΟΓ ΕΝΑΛΛΑΚΤΙΚ'
    pros_party_names[12] = 'ΑΝΕΞΑΡΤΗΤ ΕΛΛΗΝ'
    pros_party_names[13] = 'ΧΡΥΣ ΑΥΓ'
    pros_party_names[21] = 'ΕΛΛΗΝΙΚ ΛΥΣ'
    pros_party_names[22] = 'ΜΕΤΩΠ ΕΥΡΩΠΑΙΚ ΡΕΑΛΙΣΤΙΚ ΑΝΥΠΑΚΟ'

    # Μέθοδος για την αντικατάσταση των ονομάτων των παρατάξεων από τα διακριτά ονόματα σε ένα string
    def change_party_name(speech):
        for old_name, new_name in zip(pros_party_names, party_name_abbrev):
            speech = speech.replace(old_name, new_name)
        return speech
    
    # Εφαρμογή της μεθόδου στη στήλη με τις επεξεργασμένες ομιλίες και επιστροφή της στήλης
    return dataframe['processed_speeches'].apply(change_party_name)
