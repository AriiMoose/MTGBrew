import datetime

from django.db import models
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from tagging.registry import register
from tagging.fields import TagField
from ckeditor.fields import RichTextField

# Create your models here.

# Definiition for a deck
# Contains a series of Playset models for the mainboard and sideboard
# Contains deck prices, and other important deck details
# Check variable names for a description on the data contained in the Deck Model

GAME_FORMATS = (
		('STD', 'Standard'),
		('MDN', 'Modern'),
		('LGC', 'Legacy'),
		('VTG', 'Vintage'),
		('EDH', 'Commander/EDH'),
		('PAU', 'Pauper'),
	)

class Deck(models.Model):
	deck_name = models.CharField(max_length=40, blank=False)
	deck_format = models.CharField(max_length=10, choices=GAME_FORMATS, blank=False)
	deck_price_paper = models.IntegerField(validators=[MinValueValidator(0)])
	deck_price_online = models.IntegerField(validators=[MinValueValidator(0)])
	deck_privacy = models.BooleanField()
	deck_need_feedback = models.BooleanField()
	deck_rating	= models.IntegerField()
	deck_last_edited = models.DateTimeField(blank=False)
	deck_tags = TagField()
	deck_description = RichTextField(blank=False)
	decklist_mainboard = models.CharField(default=  "Please place each card on a new line. \n"
													"Formating Sample: \n"
													"4x Storm Crow \n"
													"4x Doom Blade",
											max_length=300, blank=False)
	decklist_sideboard = models.CharField(default=  "Please place each card on a new line. \n"
													"Formating Sample: \n"
													"4x Storm Crow \n"
													"4x Doom Blade",
											max_length=100, blank=False)
	deck_owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, blank=False)

	def __str__(self):
		return self.name

class DeckForm(ModelForm):
	class Meta:
		model = Deck
		fields = [	'deck_name', 'deck_format', 'deck_description', 'deck_privacy', 'deck_need_feedback', 
					'deck_tags', 'decklist_mainboard', 'decklist_sideboard']

register(Deck)