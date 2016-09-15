import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

# Create your models here.

# Definiition for a deck
# Contains a series of Playset models for the mainboard and sideboard
# Contains deck prices, and other important deck details
# Check variable names for a description on the data contained in the Deck Model

class Deck(models.Model):
	GAME_FORMATS = (
		('STD', 'Standard'),
		('MDN', 'Modern'),
		('LGC', 'Legacy'),
		('VTG', 'Vintage'),
		('EDH', 'Commander/EDH'),
		('PAU', 'Pauper')
	)

	deck_name = models.CharField(max_length=40)
	deck_format = models.CharField(max_length=10, choices=GAME_FORMATS)
	deck_price_paper = models.IntegerField(validators=[MinValueValidator(0)])
	deck_price_online = models.IntegerField(validators=[MinValueValidator(0)])
	deck_privacy = models.BooleanField()
	deck_need_feedback = models.BooleanField()
	deck_rating	= models.IntegerField()
	deck_last_edited = models.DateTimeField()
	deck_tags = ArrayField(models.CharField(max_length=15), null=True, blank=True)