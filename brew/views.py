from django.shortcuts import get_object_or_404, render, redirect
# Django imports
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Model imports
from models import DeckForm, Deck

# Python imports
import urllib2
import json

# Python library imports
import pygal

# MTGO card data via Cardhoarder
cardhoarder_data_url = "https://www.cardhoarder.com/affiliates/pricefile/480166"

# Load MTGJSON into memory
mtgjson_filepath = "brew/static/brew/AllCards.json"
mtgjson_data = json.load(open(mtgjson_filepath))

# Create your views here
def search(request):
	return render(request, 'brew/deck-search.html')

def deck_view(request, pk):
	deck = get_object_or_404(Deck, pk=pk)

	# Get card data for decklist
	creature_count = 0
	enchantment_count = 0
	instant_count = 0
	artifact_count = 0
	planeswalker_count = 0
	sorcery_count = 0
	land_count = 0

	parsed_mainboard = deck.decklist_mainboard.split('\n')

	for line in parsed_mainboard:
		if line is not "" or line is not None:
			
			current_card = str(line.split(" ", 1)[1]).strip()

			# Check card for types and aggregate
			if u"Creature" in mtgjson_data[current_card]['types']:
				creature_count = creature_count + 1
			
			if u"Instant" in mtgjson_data[current_card]['types']:
				instant_count = instant_count + 1

			if u"Sorcery" in mtgjson_data[current_card]['types']:
				sorcery_count = sorcery_count + 1

			if u"Enchantment" in mtgjson_data[current_card]['types']:
				enchantment_count = enchantment_count + 1

			if u"Land" in mtgjson_data[current_card]['types']:
				land_count = land_count + 1

			if u"Artifact" in mtgjson_data[current_card]['types']:
				artifact_count = artifact_count + 1

			if u"Planeswalker" in mtgjson_data[current_card]['types']:
				planeswalker_count = planeswalker_count + 1
			
		else:
			print "Empty line"


	# Create chart of card types
	cardtype_piechart = pygal.Pie()
	cardtype_piechart.title = "Card Type Breakdown"

	if instant_count > 0:
		cardtype_piechart.add('Instant', instant_count)

	if sorcery_count > 0:
		cardtype_piechart.add('Sorcery', sorcery_count)

	if enchantment_count > 0:
		cardtype_piechart.add('Enchantment', enchantment_count)

	if creature_count > 0:
		cardtype_piechart.add('Creature', creature_count)

	if planeswalker_count > 0:
		cardtype_piechart.add('Planeswalker', planeswalker_count)

	if artifact_count > 0:
		cardtype_piechart.add('Artifact', artifact_count)

	if land_count > 0:
		cardtype_piechart.add('Lands', land_count)

	return render(request, 'brew/deck-view.html', {'deck': deck, 'cardtype_chart': cardtype_piechart.render()})

@login_required
def deck_builder(request):
	if request.method == "POST":
		# Save Data
		form = DeckForm(request.POST)

		if form.is_valid():
			deck = form.save(commit=False)
			deck.deck_rating = 0
			deck.deck_owner = request.user
			deck.deck_last_edited = timezone.now()

			mtgo_data = urllib2.urlopen(cardhoarder_data_url)

			print(deck.deck_name)
			print(deck.deck_tags)
			print(deck.deck_format)
			print(deck.deck_privacy)
			print(deck.deck_need_feedback)
			print(deck.decklist_mainboard)
			print(deck.decklist_sideboard)
			print(deck.deck_price_online)
			print(deck.deck_description)
			print(deck.deck_owner)
			print(deck.deck_last_edited)

			deck.save()

			return redirect('deck-view', pk=deck.pk)

		else:
			print("INVALID FORM")	

	else:
		# Load empty form
		form = DeckForm()

	return render(request, 'brew/deck-builder.html', {'form': form})