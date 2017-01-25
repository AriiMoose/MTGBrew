from __future__ import absolute_import, unicode_literals
from .celery import app
from brew.models import Card, DigitalCardStore, PaperCardStore

import urllib2
import sys
import json

reload(sys)
sys.setdefaultencoding('utf8')

# Load MTGJSON into memory
mtgjson_filepath = "brew/static/brew/AllCards.json"
mtgjson_data = json.load(open(mtgjson_filepath))

paper_data_by_line = []
card_data_by_line = []

@app.task
def update_cards():
	print "Add new cards"
	insert_list = []

	for card in mtgjson_data:
		card = Card(card_name=card, card_price_paper=0, card_price_online=0)
		insert_list.append(card)

	Card.objects.bulk_create(insert_list)

@app.task
def price_update():
	print "Retrieving updated prices from tasks.py"
	card_names = []
	paper_insert_list = []
	digital_insert_list = []

	cardhoarder_data_url = "https://www.cardhoarder.com/affiliates/pricefile/480166"
	isleofcards_data_url = "https://www.isleofcards.com/files/prices.txt"
	paper_data = urllib2.urlopen(isleofcards_data_url)
	mtgo_data = urllib2.urlopen(cardhoarder_data_url)
	card_data = set(mtgo_data.read().splitlines())
	paper_card_data = set(paper_data.read().splitlines())

	for line in card_data:
		tmp_parsed_digital = line.split('\t')
		card_data_by_line.append(tmp_parsed_digital)
		card_set = DigitalCardStore(digital_store=tmp_parsed_digital)
		digital_insert_list.append(card_set)

	for line in paper_card_data:
		tmp_parsed_paper = line.split('\t')
		card_data_by_line.append(tmp_parsed_paper)
		card_set = PaperCardStore(paper_store=tmp_parsed_paper)
		paper_insert_list.append(card_set)

	# Clear old prices
	PaperCardStore.objects.all().delete()
	DigitalCardStore.objects.all().delete()

	# Add new prices
	PaperCardStore.objects.bulk_create(paper_insert_list)
	DigitalCardStore.objects.bulk_create(digital_insert_list)

def update_deck_cost(deck):
	deck_boards = []
	deck_boards.append(deck.decklist_mainboard)
	deck_boards.append(deck.decklist_sideboard)
	deck.deck_price_paper = 0
	deck.deck_price_online = 0
	card_data_by_line = DigitalCardStore.objects.values_list('digital_store', flat=True)
	paper_data_by_line = PaperCardStore.objects.values_list('paper_store', flat=True)

	for board in deck_boards:
		parsed_deck_board = board.split('\n')
		verified_current_card_digital = None
		verified_current_card_paper = None

		# Iterate through mainboard and check if card exists
		for line in parsed_deck_board:
			# Check if mainboard is formatted correctly
			# If yes, check if card exists
			# Else, raise an error
			try:
				current_card = str(line.split(" ", 1)[1]).strip()
				current_card_quantity = int(line.split(" ", 1)[0])
			except:
				print "Something went wrong"
			else:
				# Search vendor data for card
				for sublist in card_data_by_line:
					# If the card exists, grab it's dataset
					if current_card.lower() in (sublist_card.lower() for sublist_card in sublist):
						verified_current_card_digital = sublist
						break

				for sublist in paper_data_by_line:
					if current_card.lower() in (sublist_card.lower() for sublist_card in sublist):
						verified_current_card_paper = sublist
						break

				# If the card doesn't exist, return a Validation Error
				# Else, find price, and add it to the total
				if verified_current_card_digital is None:
					print "Cannot find digital card: " + str(current_card)
				else:
					deck.deck_price_online += float(verified_current_card_digital[5]) * current_card_quantity

				if verified_current_card_paper is None:
					print "Cannot find paper card: " + str(current_card)
				else:
					deck.deck_price_paper += float(verified_current_card_paper[5]) * current_card_quantity
		