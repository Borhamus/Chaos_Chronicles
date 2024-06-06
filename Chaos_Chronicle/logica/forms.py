# main/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Jugador, Deck, Carta

class AgregarCartaForm(forms.Form):
    carta = forms.ModelChoiceField(queryset=Carta.objects.all(), label="Seleccionar Carta")
    tipo = forms.ChoiceField(choices=[
        ('ci', 'Circulo'),
        ('cu', 'Cuadrado'),
        ('tr', 'Triangulo')
    ], label="Tipo de Carta")

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['Titulo', 'BackImage']

class JugadorCreationForm(UserCreationForm):
    class Meta:
        model = Jugador
        fields = ('username', 'email')

class CartaForm(forms.ModelForm):
    class Meta:
        model = Carta
        fields = ('Nombre', 'Ataque', 'Defensa', 'Costo', 'Imagen')
