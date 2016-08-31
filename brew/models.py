import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

# Definiition for a deck
# Contains a series of Playset models for the mainboard and sideboard
# Contains deck prices, and other important deck details
# Check variable names for a description on the data contained in the Deck Model
class Deck(models.Model)
	deck_name = models.CharField(max_length=200)
	deck_description = models.CharField(max_length=none)
	last_edit_date = models.DateTimeField('Last Edited: ')
	deck_price_online = models.DecimalField(max_digits=none, deicmal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	deck_price_paper = models.DecimalField(max_digits=none, deicmal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	deck_privacy = models.BinaryField()
	looking_for_feedback = models.BinaryField()
	deck_format = CharField(max_length=20)
	deck_rating = IntegerField()
	deck_tags = models.ArrayField()


class User(models.Model)
	username = models.CharField(max_length=25)

class Playset(models.Model)
	card_name = models.CharField(max_length=50)
	card_quantity = models.PositiveIntegerField(validators=[MaxValueValidator(Integer('4'))])
	card_price_online = models.DecimalField(max_digits=none, deicmal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	card_price_paper = models.DecimalField(max_digits=none, deicmal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	card_printing = models.CharField(max_length=100)
	card_condition = models.CharField(max_length=10)
	card_foil = models.BinaryField()

