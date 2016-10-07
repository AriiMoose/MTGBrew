from django import forms

from tagging.forms import TagField
from brew.models import GAME_FORMATS
from ckeditor.widgets import CKEditorWidget

class DeckForm(forms.Form):
	deck_name = forms.CharField(max_length=40, label='Deck Name')
	deck_tags = TagField(label='Deck Tags')
	deck_description = forms.CharField(max_length=1000, widget=CKEditorWidget())
	deck_format = forms.CharField(max_length=10, widget=forms.Select(choices=GAME_FORMATS))
	deck_privacy = forms.BooleanField(label='Is Private')
	deck_need_feedback = forms.BooleanField(label='Needs Feedback')
	decklist_mainboard = forms.CharField(label='Mainboard', widget=forms.Textarea)
	decklist_sideboard = forms.CharField(label='Sideboard',
										widget=forms.Textarea)