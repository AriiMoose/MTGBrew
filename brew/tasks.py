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
	paper_data_by_line = []
	card_data_by_line = []
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
		card_set = DigitalCardStore(digital_store=tmp_parsed_digital)
		digital_insert_list.append(card_set)

	for line in paper_card_data:
		tmp_parsed_paper = line.split('\t')
		card_set = PaperCardStore(paper_store=tmp_parsed_paper)
		paper_insert_list.append(card_set)

	# Clear old prices
	PaperCardStore.objects.all().delete()
	DigitalCardStore.objects.all().delete()

	# Add new prices
	PaperCardStore.objects.bulk_create(paper_insert_list)
	DigitalCardStore.objects.bulk_create(digital_insert_list)

def deprecate_price_update():
	print "Retrieving updated prices from tasks.py"
	paper_data_by_line = []
	card_data_by_line = []

	cardhoarder_data_url = "https://www.cardhoarder.com/affiliates/pricefile/480166"
	isleofcards_data_url = "https://www.isleofcards.com/files/prices.txt"
	paper_data = urllib2.urlopen(isleofcards_data_url)
	mtgo_data = urllib2.urlopen(cardhoarder_data_url)
	card_data = set(mtgo_data.read().splitlines())
	paper_card_data = set(paper_data.read().splitlines())

	for line in card_data:
		tmp_parsed_digital = line.split('\t')
		card_data_by_line.append(tmp_parsed_digital)

		# If the card exists, update the price
		# Otherwise, add it as a new DB entry
		try:
			card = Card.objects.get(name=tmp_parsed_digital[4])
			card.card_price_digital = tmp_parsed_digital[5]

		except:
			card = Card(card_name=tmp_parsed_digital[4], card_price_online=tmp_parsed_digital[5])

	for line in paper_card_data:
		tmp_parsed_paper = line.split('\t')
		paper_data_by_line.append(tmp_parsed_paper)

		# If the card exists, update the price
		# Otherwise, add it as a new DB entry
		try:
			card = Card.objects.get(name=tmp_parsed_paper[4])
			card.card_price_paper = tmp_parsed_paper[5]

		except:
			card = Card(card_name=tmp_parsed_paper[4], card_price_paper=tmp_parsed_paper[5])

	print Card.objects.all()