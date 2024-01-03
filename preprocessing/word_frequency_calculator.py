from nltk.probability  import FreqDist
from nltk.tokenize import word_tokenize
import pandas as pd

# Τα ονόματα των παρατάξεων όπως είναι στη στήλη του dataframe
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

# Λέξεις που εμφανίζονται με μεγάλη συχνότητα, αλλά δεν είναι keywords (κάποιες μπορεί να είναι)
irrelevant_words = ['ΕΥΧΑΡΙΣΤ', 'ΔΗΜΟΣΙ', 'ΚΥΒΕΡΝΗΣ',
                     'ΔΕΥΤΕΡ', 'ΕΙΔΙΚ', 'ΚΡΑΤ', 
                     'ΤΡΟΠ', 'ΥΠΗΡΕΣΙ', 'ΕΛΛΑΔ', 
                     'ΕΠΙΤΡΟΠ', 'ΕΛΛΗΝΙΚ', 'ΣΤΟΙΧΕΙ', 
                     'ΣΧΕΣ', 'σ', 'ΗΘΕΛ', 
                     'γι', 'ΠΡΟΗΓΟΥΜΕΝ', 
                     'ΛΕΜ', 'ΠΡΑΓΜΑΤΙΚ', 'ΝΟΜΙΖ', 
                     'ΘΕΜΑΤ', 'ΠΕΡΙΟΧ', 'ΕΓΙΝ', 
                     'ΓΙΝΕΤΑ', 'ΣΧΕΤΙΚ', 'ΒΕΒΑΙ', 
                     'ΑΡΙΘΜ', 'ΠΟΛΙΤ', 'ΧΡΟΝ', 
                     'ΕΡΩΤΗΣ', 'ΑΠΟΦΑΣ', 'ΔΙΑΔΙΚΑΣΙ', 
                     'ΒΟΥΛ', 'ΒΟΥΛΕΥΤ', 'ΥΠΟΥΡΓ', 
                     'ΥΠΟΥΡΓΕΙ', 'ΧΩΡ', 'ΠΡΟΕΔΡ', 
                     'ΑΡΘΡ', 'ΕΓΙΝ', 'ΜΕΓΑΛ', 
                     'ΠΕΡΙΠΤΩΣ', 'ΑΡΧ', 'ΘΕΣ', 
                     'ΣΥΖΗΤΗΣ', 'ΣΥΓΚΕΚΡΙΜΕΝ', 'ΛΟΓ', 
                     'ΧΡΟΝΙ','ΠΟΛΛ', 'ΘΕΛ', 
                     'ΑΦΟΡ', 'ΚΥΡΙ', 'ΠΟΛΙΤΙΚ', 
                     'ΓΙΑΤΙ', 'Κ', 'ΥΠΑΡΧ', 
                     '’', 'ΝΕ', '%', 
                     'ΘΕΜ', 'ΚΑΝ', 'ΕΙΠ', 
                     'ΔΙΟΤ', 'ΛΕ', 'ΔΥΟ', 
                     'ΠΡΩΤ', 'Π', 'ΣΥΝΑΔΕΛΦ', 
                     'ΓΙΝ', 'ΤΡΟΠΟΛΟΓΙ', 'ΣΤΙΓΜ',
                     'ΜΕΡ', 'ΤΕΛΕΥΤΑΙ', 'ΣΗΜΑΝΤΙΚ',
                     'ΧΙΛΙΑΔ', 'ΚΟΜΜΑΤ', 'ΔΙΑΤΑΞ',
                     'ΑΠΑΝΤΗΣ', 'ΓΕΝΙΚ', 'ΣΤΙΓΜ',
                     '`', 'ΚΑΝΕΤ', 'ΦΥΣΙΚ',
                     'ΑΠΟΨ', '+', 'ΚΑΝΟΥΜ',
                     'ΕΚΑΝ', 'Δ', 'Σ', 'ΠΑΡ',
                     'σ`', '/', 'Ν', 'Γ', 'σ’', 
                     'Β', 'γι’', 'ΟΤ', 'Τ', 'ΜΗΝ',
                     'ΠΛΕΥΡ', 'ΠΡΑΓΜΑΤΙ', 'ΠΑΝΩ', 
                     'ΑΠΛ', 'ΠΙΣΤΕΥ', 'ΒΑΣ', 
                     'ΙΔΙΑΙΤΕΡ', 'ΩΡ', 'ΜΙΚΡ', 
                     'ΣΙΓΟΥΡ', 'ΠΟΣ', 'ΑΚΟΥΣ', 
                     'ΜΠΟΡΟΥΜ', 'ΣΗΜΑΣΙ', 'ΑΝΩ', 
                     'ΚΑΛΥΤΕΡ', 'ΠΕΙΤ', 'ΘΕΛΕΤ',
                     'ΕΠΡΕΠ', 'ΑΝΑΦΕΡΕΤΑ', 'ΠΟΥΜ', 'ΑΓΑΠΗΤ', 'ΛΕΤ', 'ΔΕ', 'ΔΥΝΑΤ', 'ΠΑΡΟΝΤ', 'ΕΚ', 'ΣΗΜΕΙ', 'ΖΗΤ', 'ΑΙΘΟΥΣ', 'ΠΑΡΑΓΡΑΦ', 'ΕΝΝΟΙ']




def custom_dataframe_freq(dataframe, party = None, year = None, member = None, topk = 40):
    """
    Υπολογισμός των συχνοτήτων εμφάνισης κάθε λέξης στα επιλεγμένα speeches
    """
    #dataframe = filter_dataframe(dataframe, party, year, member)
    if party is not None and party in political_parties:
        #print('party ok')
        dataframe = dataframe[dataframe['political_party'] == party]
    if year is not None: # and year > 1988:
        #print('year ok')
        dataframe = dataframe[dataframe['year'] == year]
    if member is not None:
        #print('member OK')
        dataframe = dataframe[dataframe['member_name'] == member]
    if not dataframe.empty:
        words = [word for speech in dataframe['processed_speeches'] for word in word_tokenize(speech, preserve_line=True) if word not in irrelevant_words]

        dataframe = pd.DataFrame(FreqDist(words).most_common(topk), columns=['words', 'frequency'])
            
    return dataframe

def filter_dataframe(dataframe, party = None, year = None, member = None):
    """
    Filter dataframe based on the paramaters of the method. Returns the column of the processed speeches
    """
    if party is not None and party in political_parties:
        #print('party ok')
        dataframe = dataframe[dataframe['political_party'] == party]
    if year is not None: # and year > 1988:
        #print('year ok')
        dataframe = dataframe[dataframe['year'] == year]
    if member is not None:
        #print('member OK')
        dataframe = dataframe[dataframe['member_name'] == member]
    return dataframe['processed_speeches']
