# main/views.py
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import JugadorCreationForm, CartaForm, DeckForm, AgregarCartaForm
from .models import Carta, Deck, Jugador, DeckCard, Partida
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic import TemplateView, ListView

def deck_create(request):
    if request.method == 'POST':
        deck_form = DeckForm(request.POST, request.FILES)
        if deck_form.is_valid():
            deck = deck_form.save(commit=False)
            deck.Puntos = 100  # Inicializar con 100 puntos
            deck.save()
            deck_form.save_m2m()
            return redirect('deck_detail', deck_id=deck.id)
    else:
        deck_form = DeckForm()
    cartas = Carta.objects.all()
    return render(request, 'deck_form.html', {'deck_form': deck_form, 'cartas': cartas})

def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)

    if request.method == 'POST':
        carta_id = request.POST.get('carta_id')
        tipo = request.POST.get('tipo')
        action = request.POST.get('action')

        print(f"POST Data: carta_id={carta_id}, tipo={tipo}, action={action}")

        if action == 'add':
            try:
                carta = Carta.objects.get(id=carta_id)
                DeckCard.objects.create(deck=deck, carta=carta, tipo=tipo)
            except Carta.DoesNotExist:
                print(f"Carta with id {carta_id} does not exist.")
            except Exception as e:
                print(f"Unexpected error: {e}")
        elif action == 'remove':
            try:
                deck_card = DeckCard.objects.get(id=carta_id)
                deck_card.delete()
            except DeckCard.DoesNotExist:
                print(f"DeckCard with id {carta_id} does not exist.")
            except Exception as e:
                print(f"Unexpected error: {e}")

        deck.contar_cartas_por_tipo()
        return redirect('deck_detail', deck_id=deck.id)


    cartas = Carta.objects.all()
    deck_cards = deck.deckcard_set.all()
    return render(request, 'deck_detail.html', {
        'deck': deck,
        'cartas': cartas,
        'deck_cards': deck_cards
    })

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
        context['jugadores'] = Jugador.objects.all().order_by('ScoreTotal').values()[:10]
        return context

class CartaListView(ListView):
    model = Carta
    template_name = 'carta_list.html'
    context_object_name = 'cartas'

    def get_queryset(self):
        return Carta.objects.values('Nombre', 'Ataque', 'Defensa', 'Costo', 'Imagen')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carta_form'] = AgregarCartaForm(self.request.POST or None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        carta_form = context['carta_form']
        if carta_form.is_valid():
            deck = form.save(commit=False)
            deck.save()
            form.save_m2m()
            
            # Agregar carta al deck
            carta = carta_form.cleaned_data['carta']
            tipo = carta_form.cleaned_data['tipo']
            DeckCard.objects.create(deck=deck, carta=carta, tipo=tipo)
            deck.contar_cartas_por_tipo()
            
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

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

