import csv
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IRProject.settings")
django.setup()

from IRWebApp.models import Speech  

# Function to import data from CSV
def import_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Speech.objects.create(
                member_name=row['member_name'],
                political_party = row['political_party'],
                sitting_date = row['year'],
                speech = row['speech'],
                processed_speech = row['processed_speeches']
            )

# Execute the function
csv_file_path = 'processedspeechfinal.csv'
import_data_from_csv(csv_file_path)
