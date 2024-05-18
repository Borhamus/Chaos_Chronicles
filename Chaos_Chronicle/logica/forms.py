# main/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Jugador, Deck, Carta


class JugadorCreationForm(UserCreationForm):
    class Meta:
        model = Jugador
        fields = ('username', 'email', 'ScoreTotal', 'Decks', 'FotoPerfil')

class CartaForm(forms.ModelForm):
    class Meta:
        model = Carta
        fields = '__all__'

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = '__all__'
