import csv
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IRProject.settings")
django.setup()

from IRWebApp.models import PartyKeywords  # Import the PartyKeywords model

# Function to import data from CSV
def import_data_from_csv(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            PartyKeywords.objects.create(
                political_party=row['political_party'],
                year = row['year'],
                keywords = row['keywords']
            )

# Execute the function
csv_file_path = 'party_keywordsfinal.csv'
import_data_from_csv(csv_file_path)
