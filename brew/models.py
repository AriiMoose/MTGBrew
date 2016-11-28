import datetime

from django.db import models
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from tagging.registry import register
from tagging.fields import TagField
from ckeditor.fields import RichTextField

import json
import re
import time
import urllib2
from redactor.fields import RedactorField

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

cardhoarder_data_url = "https://www.cardhoarder.com/affiliates/pricefile/480166"
isleofcards_data_url = "https://www.isleofcards.com/files/prices.txt"
paper_data = urllib2.urlopen(isleofcards_data_url)
mtgo_data = urllib2.urlopen(cardhoarder_data_url)
card_data = set(mtgo_data.read().splitlines())
paper_card_data = set(paper_data.read().splitlines())
paper_data_by_line = []
card_data_by_line = []

for line in card_data:
	card_data_by_line.append(line.split('\t'))

for line in paper_card_data:
	paper_data_by_line.append(line.split('\t'))

class Deck(models.Model):
	deck_name = models.CharField(max_length=200, blank=False)
	deck_format = models.CharField(max_length=50, choices=GAME_FORMATS, blank=False)
	deck_price_paper = models.IntegerField(validators=[MinValueValidator(0)], default=0)
	deck_price_online = models.IntegerField(validators=[MinValueValidator(0)], default=0)
	deck_privacy = models.BooleanField(blank=True)
	deck_need_feedback = models.BooleanField(blank=True)
	deck_rating	= models.IntegerField()
	deck_last_edited = models.DateTimeField()
	deck_tags = TagField(blank=True)
	deck_description = RedactorField(verbose_name=u'Deck Description')
	decklist_mainboard = models.CharField(max_length=1000, blank=False)
	decklist_sideboard = models.CharField(max_length=1000, blank=True)
	deck_owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=None)

class DeckForm(ModelForm):
	class Meta:
		model = Deck
		fields = [	'deck_name', 'deck_format', 'deck_description', 'deck_privacy', 'deck_need_feedback', 
					'deck_tags', 'decklist_mainboard', 'decklist_sideboard']

	# Custom validation to clean the mainboard from
	#		the deck builder view
	def clean_decklist_mainboard(self):
		# Grab decklist from the form
		mainboard_buffer = self.cleaned_data.get('decklist_mainboard')

		# Check that the mainboard actually contains cards
		if mainboard_buffer == "" or mainboard_buffer == None:
			raise ValidationError(_("Your mainboard must contain cards"), code='EmptyList')
		else:
			self.parse_board(mainboard_buffer)

		return mainboard_buffer

	def clean_decklist_sideboard(self):
		sideboard_buffer = self.cleaned_data.get('decklist_sideboard')

		# Verify that the sideboard contains cards
		if sideboard_buffer == "" or sideboard_buffer == None:
			return sideboard_buffer
		else:
			self.parse_board(sideboard_buffer)

		return sideboard_buffer

	def parse_board(self, deck_board):
		parsed_deck_board = deck_board.split('\n')

		# Iterate through mainboard and check if card exists
		for line in parsed_deck_board:
			# Check if mainboard is formatted correctly
			# If yes, check if card exists
			# Else, raise an error
			try:
				current_card = str(line.split(" ", 1)[1]).strip()
				current_card_quantity = int(line.split(" ", 1)[0])
			except:
				raise ValidationError("Please provide an amount for each card entry. Example: \n 1 Storm Crow")
			else:
				# Search vendor data for card
				for sublist in card_data_by_line:
					# If the card exists, grab it's dataset
					if current_card.lower() in (sublist_card.lower() for sublist_card in sublist):
						verified_current_card = sublist
						break

				# If the card doesn't exist, return a Validation Error
				# Else, find price, and add it to the total
				if verified_current_card is None:
					raise ValidationError("Cannot find card: " + current_card)
				else:
					self.instance.deck_price_online += float(verified_current_card[5]) * current_card_quantity
register(Deck)