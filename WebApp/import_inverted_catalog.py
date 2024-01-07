import json
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IRProject.settings")
django.setup()

from IRWebApp.models import InvertedCatalog 

def import_json_data():
    with open('inverted_catalogfinal_string.json', 'r') as json_file:
        data = json.load(json_file)
        
        for unique_word, indices in data.items():
            InvertedCatalog.objects.create(
            word =  unique_word,
            speech_indices = indices
            )
            

import_json_data()