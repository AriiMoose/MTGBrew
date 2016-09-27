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
	form = DeckForm()
	return render(request, 'brew/deck-builder.html', {'form': form})