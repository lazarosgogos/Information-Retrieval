from django.db import models

# Create your models here.
class Speech(models.Model):
    member_name = models.CharField(max_length=100)
    political_party = models.CharField(max_length=100)
    sitting_date = models.IntegerField()
    speech = models.TextField()
    processed_speech = models.TextField()

class PartyKeywords(models.Model):
    political_party = models.CharField(max_length=100)
    year = models.IntegerField()
    keywords = models.TextField()

class MemberKeywords(models.Model):
    member_name = models.CharField(max_length=100)
    year = models.IntegerField()
    keywords = models.TextField()


class SimilarMembers(models.Model):
    member_name = models.CharField(max_length = 100)
    similar_members = models.TextField()

class InvertedCatalog(models.Model):
    word = models.CharField(max_length = 100)
    speech_indices = models.TextField()

