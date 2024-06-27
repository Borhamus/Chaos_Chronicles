# main/views.py
from django.shortcuts import redirect, render, get_object_or_404
from django import template
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import JugadorCreationForm, CartaForm, DeckForm, DeckForm2
from .models import Carta, Deck, Jugador, DeckCard, Partida
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

#def ChangeBackImage(request, deck_id):
#
#    deck = get_object_or_404(Deck, id=deck_id)
#
#    if request.method == 'POST':
#        deck_form = DeckForm2(request.POST, request.FILES)
#        if deck_form.is_valid():
#            deck = deck_form.save(commit=False)
#            deck.save()
#            deck_form.save_m2m() 
#            return redirect('deck_detail', deck_id=deck.id)
#    else:
#        deck_form = DeckForm2()
#    return render(request, 'deck_detail.html', {'form': deck_form})

class DeckListView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = 'deck_list.html'
    context_object_name = 'decks'

    #Obtiene todos los decks que pertenezcan al Jugador - Usuario
    def get_queryset(self):
        usuario = self.request.user
        decks = usuario.Decks.all()
        return decks
    
    #Permite al usuario seleccionar un deck en especifico
    def post(self, request, *args, **kwargs):
        deck_id = request.POST.get('deck_id')
        deck = Deck.objects.get(id=deck_id)
        usuario = request.user
        usuario.deck_seleccionado = deck
        usuario.save()
        return redirect('deck_list')
    
    #Obtiene el deck seleccionado por el ususario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck_seleccionado'] = self.request.user.deck_seleccionado if hasattr(self.request.user, 'deck_seleccionado') else None
        return context

@login_required
def eliminar_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    
    if request.method == 'POST':
        deck.delete()
    
    return redirect('deck_list')
    
        
    
class DeckCreateView(LoginRequiredMixin, CreateView):
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

@login_required
def deck_create(request):
    if request.method == 'POST':
        deck_form = DeckForm(request.POST, request.FILES)
        if deck_form.is_valid():
            deck = deck_form.save(commit=False)
            deck.Puntos = 100  # Inicializar con 100 puntos
            deck.save()
            deck_form.save_m2m()

            #Asigna el deck creado al usuario
            request.user.Decks.add(deck)
            return redirect('deck_detail', deck_id=deck.id)
        
    else:
        deck_form = DeckForm()
    return render(request, 'deck_create.html', {'form': deck_form})

@login_required
def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    
    #Verifica si el usuario registrado posee el deck a visualizar.
    if deck not in request.user.Decks.all():
        return HttpResponseForbidden("No existe este deck.")

    if request.method == 'POST':
        carta_id = request.POST.get('carta_id')
        tipo = request.POST.get('tipo')
        action = request.POST.get('action')
        
        if tipo == 'ci':
            imagenTipo = 'tipes/Circulo.png'
        elif tipo == 'cu':
            imagenTipo = 'tipes/Cuadrado.png'
        elif tipo == 'tr':
            imagenTipo = 'tipes/Triangulo.png'

    

        print(f"POST Data: carta_id={carta_id}, tipo={tipo}, action={action}")

        if action == 'add':
            try:
                carta = Carta.objects.get(id=carta_id)
                DeckCard.objects.create(deck=deck, carta=carta, tipo=tipo, imagenTipo=imagenTipo)
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
    return render(request, 'deck_detail.html',{
        'deck': deck,
        'cartas': cartas,
        'deck_cards': deck_cards,
        'range':range(deck.CantidadCartas,21),
    })

def copiar_cartas(request, origen_deck_id):
    origen_deck = get_object_or_404(Deck, id=origen_deck_id)
    # Obtener las cartas asociadas al mazo de origen
    copied_cartas = list(DeckCard.objects.filter(deck=origen_deck).values('carta_id', 'tipo'))
    request.session['copied_cartas'] = copied_cartas
    messages.success(request, 'Cartas copiadas exitosamente del deck {0}.'.format(origen_deck.Titulo))
    next_url = request.GET.get('next', 'deck_list')
    return redirect(next_url)

@login_required
def pegar_cartas(request, destino_deck_id):
    destino_deck = get_object_or_404(Deck, id=destino_deck_id)
    copied_cartas = request.session.get('copied_cartas', [])
    deck_cards = DeckCard.objects.filter(deck=destino_deck)

    if not copied_cartas:
        messages.error(request, 'No hay cartas copiadas.')
        next_url = request.GET.get('next', 'deck_list')
        return redirect(next_url)

    for deck_card in deck_cards:
        deck_card.delete()

    for carta_data in copied_cartas:
        carta = get_object_or_404(Carta, id=carta_data['carta_id'])
        if carta_data['tipo'] == 'ci':
            imagenTipo = 'tipes/Circulo.png'
        elif carta_data['tipo'] == 'cu':
            imagenTipo = 'tipes/Cuadrado.png'
        elif carta_data['tipo'] == 'tr':
            imagenTipo = 'tipes/Triangulo.png'
        DeckCard.objects.create(deck=destino_deck, carta=carta, tipo=carta_data['tipo'], imagenTipo=imagenTipo)
    
        

    messages.success(request, 'Cartas pegadas exitosamente al deck {0}.'.format(destino_deck.Titulo))
    del request.session['copied_cartas']  # Clear copied cartas from session
    destino_deck.contar_cartas_por_tipo()
    return redirect('deck_detail', deck_id=destino_deck.id)    

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

        # Obtener el usuario actual
        usuario = self.request.user

        #Obtener los jugadores con el mayor ScoreTotal
            # Context['jugadores'] se refiere al nombre que tendrá en el contexto de la template.
            # Jugador.objects.all() obtiene todos los jugadores de la DB.
            # order_by('-ScoreTotal') Ordena de forma DESCENDIENTE a los jugadores según su Score.
            # values()[:5] Muestra 5 valores y los devuelve en forma de diccionario.
        context['jugadores']=Jugador.objects.all().order_by('-ScoreTotal').values()[:5]

        # Añadir el deck seleccionado del usuario al contexto
        context['deck_seleccionado'] = usuario.deck_seleccionado if hasattr(usuario, 'deck_seleccionado') else None

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

# PEDRO PEDRO PEDRO