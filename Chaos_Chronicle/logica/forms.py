# main/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Jugador, Deck, Carta, DeckCard


class DeckSeleccionForm(forms.Form):
    deck = forms.ModelChoiceField(queryset=Deck.objects.all(), label="Selecciona un deck")

class AgregarCartaForm(forms.Form):
    class Meta:
        model = DeckCard
    
    carta = forms.ModelChoiceField(queryset=Carta.objects.all(), label="Seleccionar Carta")
    tipo = forms.ChoiceField(choices=[
        ('ci', 'Circulo'),
        ('cu', 'Cuadrado'),
        ('tr', 'Triangulo')
    ], label="Tipo de Carta")

    # TODO: validacion
    # def clean_carta(self):
    #     carta = self.cleaned_data.get('carta')
    #     deck = self.cleaned_data.get('deck')
    #     cantidad_cartas = deck.cartas.filter(pk=carta.id)
    #     if cantidad_cartas == 2:
    #         raise forms.ValidationError("Esta carta ya fue agregada 2 veces.")
    #     return carta

# Definir las opciones de imágenes predefinidas
IMAGE_CHOICES = [
    ('backimages/A.png', 'Imagen 1'),
    ('backimages/B.png', 'Imagen 2'),
    ('backimages/C.png', 'Imagen 3'),
    ('backimages/D.png', 'Imagen 4'),
    # añadir tantas opciones como necesites
]

class DeckForm(forms.ModelForm):
    BackImage = forms.ChoiceField(choices=IMAGE_CHOICES, label="Selecciona una imagen de fondo")

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
