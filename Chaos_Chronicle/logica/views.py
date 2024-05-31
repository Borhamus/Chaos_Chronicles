# main/views.py
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import JugadorCreationForm, CartaForm, DeckForm
from .models import Carta, Deck, Jugador, Partida #PartidaJugador armar cuando exista el juego
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic import TemplateView, ListView

def home(request):
    top_players = Jugador.objects.order_by('-ScoreTotal')[:3]
    return render

class DeckCreateView(CreateView):
    model = Deck
    form_class = DeckForm
    template_name = 'deck_form.html'
    success_url = reverse_lazy('deck_list')

    def form_valid(self, form):
        deck = form.save(commit=False)
        deck.PuntosRestantes = 100  # Inicializar con 100 puntos
        deck.save()
        form.save_m2m()
        return super().form_valid(form)

def deck_create(request):
    if request.method == 'POST':
        form = DeckForm(request.POST, request.FILES)
        if form.is_valid():
            deck = form.save(commit=False)
            deck.PuntosRestantes = 100  # Inicializar con 100 puntos
            deck.save()
            form.save_m2m()
            return redirect('deck_list')
    else:
        form = DeckForm()
    cartas = Carta.objects.all()
    return render(request, 'deck_form.html', {'form': form, 'cartas': cartas})

def logout_view(request):
    logout(request)
    return redirect('home')

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = JugadorCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    

class HomeView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jugadores']=Jugador.objects.obetener_10_mejores()
        return context

class CartaListView(ListView):
    model = Carta
    template_name = 'carta_list.html'
    context_object_name = 'cartas'

    def get_queryset(self):
        return Carta.objects.values('Nombre', 'Ataque', 'Defensa', 'Costo', 'Imagen',)

class CartaCreateView(CreateView):
    model = Carta
    form_class = CartaForm
    template_name = 'carta_form.html'
    success_url = reverse_lazy('carta_list')

class DeckListView(ListView):
    model = Deck
    template_name = 'deck_list.html'
    context_object_name = 'decks'

class DeckEditView(UpdateView):
    model = Deck
    form_class = DeckForm
    template_name = 'deck_form.html'
    success_url = reverse_lazy('deck_list')
    pk_url_kwarg = 'deck_id'

class TutorialView(TemplateView):
    template_name = 'tutorial.html'

class LeaderboardView(ListView):
    model = Jugador
    template_name = 'leaderboard.html'
    context_object_name = 'jugadores'
    ordering = ['-ScoreTotal']

class PartidaListView(ListView):
    model = Partida
    template_name = 'partida_list.html'
    context_object_name = 'partidas'

class PartidaCreateView(CreateView):
    model = Partida
    template_name = 'partida_form.html'
    success_url = reverse_lazy('partida_list')
    # Añade fields y form_class cuando definas el formulario de Partida


'''
############################################################################## Por si acaso: borrador viejo:

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
    cartas = Carta.objects.values('Nombre', 'Ataque', 'Defensa', 'Costo', 'Imagen')
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
'''
