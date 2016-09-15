from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required

# Create your views here.
def search(request):
	return render(request, 'brew/deck-search.html')

def deck_builder(request):
	return render(request, 'brew/deck-builder.html')

#def user_login_register(request):

	# Log the user in
	#user = authenticate(username=username, password=password)

	#if user is not None:
		# Login successful
		# Redirect

	#else:
		# Login invalid
		# Display error