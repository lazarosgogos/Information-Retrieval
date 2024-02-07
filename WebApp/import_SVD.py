# import json
import os
import django
import pickle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IRProject.settings")
django.setup()

from IRWebApp.models import SVD 

def import_pkl_data():
    with open('per_speech_keywords.pkl', 'rb') as json_file:
        data = pickle.load(json_file)
        
        for docId, keywords in data.items():
            SVD.objects.create(
                speech_indices =  docId, # this should be named speech_index not indices
                speech_keywords = keywords
            )
            

import_pkl_data()