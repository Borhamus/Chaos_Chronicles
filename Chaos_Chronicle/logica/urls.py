# main/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    RegisterView, CustomLoginView, HomeView, CartaListView, CartaCreateView, DeckListView, DeckEditView,
    LeaderboardView, PartidaListView, PartidaCreateView, logout_view, deck_create, deck_detail
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('cartas/', CartaListView.as_view(), name='carta_list'),
    path('cartas/nueva/', CartaCreateView.as_view(), name='carta_create'),
    path('decks/', login_required(DeckListView.as_view()), name='deck_list'),
    path('decks/nuevo/', deck_create, name='deck_create'),
    path('decks/editar/<int:deck_id>/', DeckEditView.as_view(), name='deck_edit'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('partidas/', PartidaListView.as_view(), name='partida_list'),
    path('partidas/nueva/', PartidaCreateView.as_view(), name='partida_create'),
    path('decks/ver/<int:deck_id>/', deck_detail, name='deck_detail'),
]