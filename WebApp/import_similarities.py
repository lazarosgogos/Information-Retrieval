import json
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IRProject.settings")
django.setup()

from IRWebApp.models import SimilarMembers 

def import_json_data():
    with open('member_similaritiesfinal.json', 'r') as json_file:
        data = json.load(json_file)
        
        for name, similar in data.items():
            SimilarMembers.objects.create(
            member_name =  name,
            similar_members = similar
            )
            

import_json_data()