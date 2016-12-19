"""mtgbrew URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from brew import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^$', views.search, name='search'),
    url(r'^deck-builder/', views.deck_builder, name ='deck-builder'),
    url(r'^(?P<username>\w+)/my-decks', views.my_decks, name='my-decks'),
    url(r'^deck/(?P<pk>\d+)/$', views.deck_view, name ='deck-view'),
    url(r'^deck/(?P<pk>\d+)/edit/$', views.deck_edit, name="deck-edit"),
    url(r'^deck/(?P<pk>\d+)/delete/$', views.deck_delete, name="deck-delete"),
    url(r'^accounts/', include('allauth.urls')),
]