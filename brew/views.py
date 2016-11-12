from django.shortcuts import get_object_or_404, render, redirect
# Django imports
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Model imports
from models import DeckForm

# Python imports
import urllib2

# MTGO card data via Cardhoarder
cardhoarder_data_url = "https://www.cardhoarder.com/affiliates/pricefile/480166"

# Create your views here.
def search(request):
	return render(request, 'brew/deck-search.html')

def deck_view(request, pk):
	deck = get_object_or_404(DeckForm, pk=pk)
	return render(request, 'brew/deck-view.html', {'deck': deck})

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

		else:
			print("INVALID FORM")	

	else:
		# Load empty form
		form = DeckForm()

	return render(request, 'brew/deck-builder.html', {'form': form})