# main/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    RegisterView, CustomLoginView, HomeView, CartaListView, CartaCreateView, DeckListView,
    LeaderboardView, PartidaListView, PartidaCreateView, logout_view, deck_create, 
    deck_detail, eliminar_deck, pegar_cartas, copiar_cartas, change_backimage, UserProfileView, EditUserProfileView, ChangePasswordView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('cartas/', CartaListView.as_view(), name='carta_list'),
    path('cartas/nueva/', CartaCreateView.as_view(), name='carta_create'),
    path('decks/', login_required(DeckListView.as_view()), name='deck_list'),
    path('decks/nuevo/', deck_create, name='deck_create'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('partidas/', PartidaListView.as_view(), name='partida_list'),
    path('partidas/nueva/', PartidaCreateView.as_view(), name='partida_create'),
    path('decks/ver/<int:deck_id>/', deck_detail, name='deck_detail'),
    path('deck/eliminar/<int:deck_id>/', eliminar_deck, name='eliminar_deck'),
    path('deck/copiar_cartas/<int:origen_deck_id>/', copiar_cartas, name='copiar_cartas'),
    path('deck/pegar_cartas/<int:destino_deck_id>/', pegar_cartas, name='pegar_cartas'),
    path('deck/changebackimage/<int:change_deck_id>/', change_backimage, name='change_backimage'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', EditUserProfileView.as_view(), name='edit_user_profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change_password'),
]