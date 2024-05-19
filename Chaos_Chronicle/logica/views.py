# main/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import JugadorCreationForm, CartaForm, DeckForm
from .models import Carta, Deck, Jugador, Partida, PartidaJugador
from django.http import HttpResponse



def register(request):
    if request.method == 'POST':
        form = JugadorCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = JugadorCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def home(request):
    return render(request, 'home.html')

# Funcionalidades de cartas y mazos
def carta_list(request):
    cartas = Carta.objects.all()
    return render(request, 'carta_list.html', {'cartas': cartas})

# Yo no se si quiero crear cartas dentro del proyecto, osea... si, para crearlas... 
#pero seria mejor armar un programa que las crea de una.
#Como un .bat que las cargue y ya. total, tenemos el nombre, 
#los valores, la imagen url, y todo en una lista de cada carta,
#seguida de un enter, tipo archivo.
def carta_create(request):
    if request.method == 'POST':
        form = CartaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('carta_list')
    else:
        form = CartaForm()
    return render(request, 'carta_form.html', {'form': form})

def deck_list(request):
    decks = Deck.objects.all()
    return render(request, 'deck_list.html', {'decks': decks})

def deck_create(request):
    if request.method == 'POST':
        form = DeckForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('deck_list')
    else:
        form = DeckForm()
    return render(request, 'deck_form.html', {'form': form})

def deck_edit(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        form = DeckForm(request.POST, request.FILES, instance=deck)
        if form.is_valid():
            form.save()
            return redirect('deck_list')
    else:
        form = DeckForm(instance=deck)
    return render(request, 'deck_form.html', {'form': form, 'deck': deck})

def tutorial(request):
    return render(request, 'tutorial.html')

def leaderboard(request):
    jugadores = Jugador.objects.all().order_by('-ScoreTotal')
    return render(request, 'leaderboard.html', {'jugadores': jugadores})

def partida_list(request):
    partidas = Partida.objects.all()
    return render(request, 'partida_list.html', {'partidas': partidas})

def partida_create(request):
    if request.method == 'POST':
        # Lógica para crear una nueva partida
        pass
    return render(request, 'partida_form.html')