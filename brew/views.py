from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from forms import DeckForm

# Create your views here.
def search(request):
	return render(request, 'brew/deck-search.html')

@login_required
def deck_builder(request):
	if request.method == "POST":
		# Save Data
		form = DeckForm()

		if form.is_valid():
			# Save data from Form driven fields
			deck = form.save(commit=false)

			# Save Data from HTML driven fields
			deck.deck_name = form.cleaned_up['deck-name']
			deck.deck_tags = form.cleaned_up['deck-tags']
			deck.deck_privacy = form.cleaned_up['is-private']
			deck.deck_need_feedback = form.cleaned_up['need-feedback']
			deck.deck_mainboard = form.cleaned_up['mainboard']
			deck.deck_sideboard = form.cleaned_up['sideboard']
			deck.deck_owner = request.user
			deck.deck_last_edited = timezone.now()

			deck.save()

	else:
		# Load empty form
		form = DeckForm()

	return render(request, 'brew/deck-builder.html', {'form': form})