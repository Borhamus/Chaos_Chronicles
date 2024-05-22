# main/urls.py
from django.urls import path, include
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('', home, name='home'),
    path('cartas/', carta_list, name='carta_list'),
    path('cartas/nueva/', carta_create, name='carta_create'),
    path('decks/', deck_list, name='deck_list'),
    path('decks/nuevo/', deck_create, name='deck_create'),
    path('decks/editar/<int:deck_id>/', deck_edit, name='deck_edit'),
    path('tutorial/', tutorial, name='tutorial'),
    path('leaderboard/', leaderboard, name='leaderboard'),
    path('partidas/', partida_list, name='partida_list'),
    path('partidas/nueva/', partida_create, name='partida_create'),
]
