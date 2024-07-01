# main/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
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

class DeckForm2(forms.ModelForm):
    BackImage = forms.ChoiceField(choices=IMAGE_CHOICES, label="Selecciona una nueva imagen de fondo")

    class Meta:
        model = Deck
        fields = ['BackImage']

class DeckForm3(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['Titulo']

class JugadorCreationForm(UserCreationForm):
    class Meta:
        model = Jugador
        fields = ('username', 'email')

class CartaForm(forms.ModelForm):
    class Meta:
        model = Carta
        fields = ('Nombre', 'Ataque', 'Defensa', 'Costo', 'Imagen')

#Formulario para editar el perfil del Usuario
class UserProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = Jugador
        fields = ['username', 'FotoPerfil']

#Formulario para editar la contraseña del usuario
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = Jugador
        fields = ['old_password', 'new_password1', 'new_password2']
