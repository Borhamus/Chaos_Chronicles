# main/views.py
from django.shortcuts import redirect, render, get_object_or_404
from django import template
from django.db.models.query import QuerySet
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import DeckForm3, JugadorCreationForm, CartaForm, DeckForm, DeckForm2, UserProfileForm, CustomPasswordChangeForm
from .models import Carta, Deck, Jugador, DeckCard, Partida,PartidaJugador
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages



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
    user = request.user
    
    # Verificar si el usuario tiene el deck en su lista de decks
    is_owner = deck in user.Decks.all()

    if request.method == 'POST':
        if not is_owner:
            return HttpResponseForbidden("No tienes permiso para modificar este deck.")
        
        carta_id = request.POST.get('carta_id')
        tipo = request.POST.get('tipo')
        action = request.POST.get('action')
        
        if tipo == 'ci':
            imagenTipo = 'tipes/Circulo.png'
        elif tipo == 'cu':
            imagenTipo = 'tipes/Cuadrado.png'
        elif tipo == 'tr':
            imagenTipo = 'tipes/Triangulo.png'
        else:
            imagenTipo = 'tipes/Default.png'  # Valor por defecto si el tipo es desconocido

        if action == 'add':
            if deck.CantidadCartas < 21:
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
    
    cartas = Carta.objects.all().order_by("Costo", "Ataque")
    deck_cards = deck.deckcard_set.all()
    
    return render(request, 'deck_detail.html', {
        'deck': deck,
        'cartas': cartas,
        'deck_cards': deck_cards,
        'range': range(deck.CantidadCartas, 21),
        'can_edit': is_owner
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

@login_required
def change_backimage(request, change_deck_id):

    deck = get_object_or_404(Deck, id=change_deck_id)

    if request.method == 'POST':
        deck_form = DeckForm2(request.POST, request.FILES)
        if deck_form.is_valid():
            deck.BackImage = deck_form.cleaned_data['BackImage']
            deck.save()
            print(f"POST Data:  deck saved")
            return redirect('deck_detail', deck_id=change_deck_id)
    else:
        deck_form = DeckForm2()
    return render(request, 'change_backimage.html', {'form': deck_form})  

@login_required
def change_deckname(request, change_deck_id):

    deck = get_object_or_404(Deck, id=change_deck_id)

    if request.method == 'POST':
        deck_form = DeckForm3(request.POST)
        if deck_form.is_valid():
            deck.Titulo = deck_form.cleaned_data['Titulo']
            deck.save()
            print(f"POST Data:  deck saved")
            return redirect('deck_detail', deck_id=change_deck_id)
    else:
        deck_form = DeckForm3()
    return render(request, 'change_deckname.html', {'form': deck_form}) 

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
        context['jugadores']= Jugador.objects.all().order_by('-ScoreTotal')[:5]

        # Añadir el deck seleccionado del usuario al contexto
        context['deck_seleccionado'] = usuario.deck_seleccionado if hasattr(usuario, 'deck_seleccionado') else None

        return context

class CartaListView(ListView):
    model = Carta
    template_name = 'carta_list.html'
    context_object_name = 'cartas'

    def get_queryset(self):
        return Carta.objects.values('Nombre', 'Ataque', 'Defensa', 'Costo', 'Imagen')


class LeaderboardView(ListView):
    model = Jugador
    template_name = 'leaderboard.html'
    context_object_name = 'jugadores'
    ordering = ['-ScoreTotal']


#Vista para el perfil del usuario
class UserProfileView(DetailView):
    model = Jugador
    template_name = 'profile_view.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return get_object_or_404(Jugador, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jugador = self.get_object()
        
        # Obtener las últimas 5 partidas en las que el jugador participó
        partidas_jugador = PartidaJugador.objects.filter(Jugador=jugador).order_by('-Partida__Fecha')[:5]
        context['partidas_jugador'] = partidas_jugador
        
        # Calcular el ranking del jugador basado en el ScoreTotal
        jugadores = Jugador.objects.all().order_by('-ScoreTotal')
        rank = list(jugadores).index(jugador) + 1
        context['rank'] = rank

        return context

#Vista para Editar el perfil del usuario
class EditUserProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Jugador
    form_class = UserProfileForm
    template_name = 'profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'pk':self.request.user.pk})

    def get_object(self):
        return self.request.user

    def test_func(self):
        return self.get_object() == self.request.user

#Vista para cambiar la contraseña del usuario
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'change_password.html'
    success_url = reverse_lazy('user_profile')  # Redirige al perfil del usuario después de cambiar la contraseña

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'pk':self.request.user.pk})


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Asegúrate de pasar el usuario al formulario
        return kwargs
# PEDRO PEDRO PEDRO