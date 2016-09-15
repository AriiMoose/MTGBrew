from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader

# Create your views here.
def search(request):
	return render(request, 'brew/deck-search.html')

def deck_builder(request):
	return render(request, 'brew/deck-builder.html')