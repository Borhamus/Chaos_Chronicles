from django.contrib import admin
from .models import Carta, Jugador, Partida, PartidaJugador, Deck

admin.site.register(Carta)
admin.site.register(Jugador)
admin.site.register(Partida)
admin.site.register(PartidaJugador)
admin.site.register(Deck)