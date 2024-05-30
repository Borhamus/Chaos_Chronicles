# main/urls.py
from django.urls import path
from .views import (
    RegisterView, CustomLoginView, HomeView, CartaListView, CartaCreateView, DeckListView, DeckCreateView, DeckEditView,
    TutorialView, LeaderboardView, PartidaListView, PartidaCreateView, logout_view,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('cartas/', CartaListView.as_view(), name='carta_list'),
    path('cartas/nueva/', CartaCreateView.as_view(), name='carta_create'),
    path('decks/', DeckListView.as_view(), name='deck_list'),
    path('decks/nuevo/', DeckCreateView.as_view(), name='deck_create'),
    path('decks/editar/<int:deck_id>/', DeckEditView.as_view(), name='deck_edit'),
    path('tutorial/', TutorialView.as_view(), name='tutorial'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('partidas/', PartidaListView.as_view(), name='partida_list'),
    path('partidas/nueva/', PartidaCreateView.as_view(), name='partida_create'),
]