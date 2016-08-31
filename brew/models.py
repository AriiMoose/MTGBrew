import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

# Definiition for a deck
class Deck(models.Model)
	deck_name = models.CharField(max_length=200)
	last_edit_date = models.DateTimeField('Last Edited: ')

class User(models.Model)
	username = models.CharField(max_length=25)
	