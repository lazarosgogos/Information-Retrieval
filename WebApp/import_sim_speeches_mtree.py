# import json
import os
import django
import pickle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IRProject.settings")
django.setup()

from IRWebApp.models import SimilarSpeeches

def import_pkl_data():
    with open('speeches_signatures.pkl', 'rb') as pkl_file:
        speeches_signatures = pickle.load(pkl_file) # a dictionary
        # key: the index of the speech
        # value: the signature of the speech
    with open('sim_tree.pkl', 'rb') as pkl_file:
        mtree = pickle.load(pkl_file) # the M-Tree
        # where the speeches are grouped together
        # and searches can take place
        # to find similar ones!
        
        
    for docId, keywords in data.items():
        SVD.objects.create(
            speech_indices =  docId,
            speech_keywords = keywords
        )
            

import_pkl_data()