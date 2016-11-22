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
from operator import itemgetter

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
	# Counters for card types
	creature_count = 0
	enchantment_count = 0
	instant_count = 0
	artifact_count = 0
	planeswalker_count = 0
	sorcery_count = 0
	land_count = 0

	card_type_counts = {"Creature": 0,
				"Enchantment": 0,
				"Instant": 0,
				"Artifact": 0,
				"Planeswalker": 0,
				"Sorcery": 0,
				"Land": 0}

	# List of all CMCs
	deck_cmc_list = []

	# Dictionary containing list of color-sorted CMCs
	card_cmc_lists = { "W": [],
				"U": [],
				"B": [],
				"R": [],
				"G": [],
				"C": []}

	parsed_decklist = deck.decklist_mainboard.split('\n')

	for line in parsed_decklist:
		if line is not "" or line is not None:
			
			current_card = str(line.split(" ", 1)[1]).strip()
			current_card_quantity = int(line.split(" ", 1)[0])

			for key, value in card_type_counts.iteritems():
				if key in mtgjson_data[current_card]['types']:
					card_type_counts[key] += current_card_quantity

			# Check for card colours and aggregate 
			# Check if card has Color Identity to account for lands 
			if 'Land' not in mtgjson_data[current_card]['types']:
				# If the card has a color ID then proceed
				# Otherwise, it's colorless
				if mtgjson_data[current_card].has_key('colorIdentity'):	
					for key, value in card_cmc_lists.iteritems():		
						if key in mtgjson_data[current_card]['colorIdentity']:
							# Attempt to retreive the CMC
							# If no CMC, set CMC to 0
							try:
								current_card_cmc = mtgjson_data[current_card]['cmc']
								deck_cmc_list.append(current_card_cmc)
								cmc_info = (current_card_cmc, current_card_quantity)
								card_cmc_lists[key].append(cmc_info)
							except:
								current_card_cmc = 0
								deck_cmc_list.append(current_card_cmc)
								cmc_info = (current_card_cmc, current_card_quantity)
								card_cmc_lists[key].append(cmc_info)
				else:
					print str(current_card) + " is colorless"
					try:
						current_card_cmc = mtgjson_data[current_card]['cmc']
						deck_cmc_list.append(current_card_cmc)
						cmc_info = (current_card_cmc, current_card_quantity)
						card_cmc_lists['C'].append(cmc_info)
					except:
						current_card_cmc = 0
						deck_cmc_list.append(current_card_cmc)
						cmc_info = (current_card_cmc, current_card_quantity)
						card_cmc_lists['C'].append(cmc_info)

	# Create chart of card types
	cardtype_piechart = pygal.Pie()
	cardtype_piechart.title = "Card Type Breakdown"

	for key, value in card_type_counts.iteritems():
		if value > 0:
			cardtype_piechart.add(key, value)

	# Create CMC bar chart
	deck_cmc_list.sort()
	

	# Check CMC values from min CMC to max CMC in list
	# CMC values in decks go from 0 to x
	# This reflects the order for elements in a list
	def sort_cmc_by_color(color):
		new_cmc = []
		for i in range(0, (deck_cmc_list[-1] + 1)):
			# Create empty entry for insertion
			new_cmc.append(None)
			# Check if any CMCs match the current CMC value to check
			for cmc in card_cmc_lists[color]:
				# If a match is found, try to add to current CMC count
				# Otherwise, insert value as initial count
				if cmc[0] == i:
					try:
						new_cmc[i] += cmc[1]
					except:
						new_cmc[i] = cmc[1]

		return new_cmc


	cmc_barchart = pygal.StackedBar()
	cmc_barchart.title = "Mana Curve"
	cmc_barchart.x_labels = map(str, range(0, deck_cmc_list[-1] + 1))
	cmc_barchart.add("White", sort_cmc_by_color("W"))
	cmc_barchart.add("Blue", sort_cmc_by_color("U"))
	cmc_barchart.add("Black", sort_cmc_by_color("B"))
	cmc_barchart.add("Red", sort_cmc_by_color("R"))
	cmc_barchart.add("Green", sort_cmc_by_color("G"))
	cmc_barchart.add("Colorless", sort_cmc_by_color("C"))

	return render(request, 'brew/deck-view.html', {'deck': deck, 'cardtype_chart': cardtype_piechart.render(), 'cmc_chart': cmc_barchart.render()})

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

			deck.save()

			return redirect('deck-view', pk=deck.pk)

		else:
			print("INVALID FORM")	

	else:
		# Load empty form
		form = DeckForm()

	return render(request, 'brew/deck-builder.html', {'form': form})