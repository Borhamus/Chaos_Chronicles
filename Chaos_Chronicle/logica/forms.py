# main/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Jugador, Deck, Carta
from .widgets import CustomCardSelectWidget


class JugadorCreationForm(UserCreationForm):
    class Meta:
        model = Jugador
        fields = ('username', 'email')

class CartaForm(forms.ModelForm):
    class Meta:
        model = Carta
        fields = ('Nombre', 'Ataque', 'Defensa', 'Costo', 'Imagen')

class DeckForm(forms.ModelForm):
    Cartas = forms.ModelMultipleChoiceField(
        queryset=Carta.objects.all(),
        widget=CustomCardSelectWidget,
        required=False,
    )

    class Meta:
        model = Deck
        fields = ['Titulo', 'Cartas']


