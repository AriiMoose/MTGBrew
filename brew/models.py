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
mtgo_data = urllib2.urlopen(cardhoarder_data_url)
card_data = set(mtgo_data.read().splitlines())
card_data_by_line = []

for line in card_data:
	card_data_by_line.append(line.split('\t'))

class Deck(models.Model):
	deck_name = models.CharField(max_length=100, blank=False)
	deck_format = models.CharField(max_length=50, choices=GAME_FORMATS, blank=False)
	deck_price_paper = models.IntegerField(validators=[MinValueValidator(0)])
	deck_price_online = models.IntegerField(validators=[MinValueValidator(0)])
	deck_privacy = models.BooleanField(blank=True)
	deck_need_feedback = models.BooleanField(blank=True)
	deck_rating	= models.IntegerField()
	deck_last_edited = models.DateTimeField()
	deck_tags = TagField(blank=True)
	deck_description = models.CharField(max_length=5000, blank=False)
	decklist_mainboard = models.CharField(max_length=500, blank=False)
	decklist_sideboard = models.CharField(max_length=500, blank=True)
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
			parsed_mainboard = mainboard_buffer.split('\n')

			# Iterate through mainboard and check if card exists
			for line in parsed_mainboard:
				# Check if mainboard is formatted correctly
				# If yes, check if card exists
				# Else, raise an error
				try:
					current_card = str(line.split(" ", 1)[1]).strip()
				except:
					raise ValidationError("Please provide an amount for each card entry. Example: \n 1 Storm Crow")
				else:
					# Search vendor data for card
					for sublist in card_data_by_line:
						# If the card exists, grab it's dataset
						if current_card in sublist:
							verified_current_card = sublist
							break

					# If the card doesn't exist, return a Validation Error
					# Else, find price, and add it to the total
					if verified_current_card is None:
						raise ValidationError("Cannot find card: " + current_card)
					else:
						print verified_current_card

		return mainboard_buffer

	def parse_board(deck_board):
		if deck_board_buffer == "" or deck_board_buffer == None:
			raise ValidationError(_("Your decklist must contain cards"), code='EmptyList')

		else:
			parsed_deck_board = deck_board_buffer.split('\n')

			# Iterate through mainboard and check if card exists
			for line in parsed_deck_board:
				# Check if mainboard is formatted correctly
				# If yes, check if card exists
				# Else, raise an error
				try:
					current_card = str(line.split(" ", 1)[1]).strip()
				except:
					raise ValidationError("Please provide an amount for each card entry. Example: \n 1 Storm Crow")
				else:
					if current_card in [elem for sublist in card_data_by_line for elem in sublist]:
						print elem
					else:
						print "Could not find card"
						raise ValidationError("Cannot find card: " + current_card)

		return deck_board_buffer

register(Deck)