from django.contrib import admin
from .models import Carta, Deck, Jugador, Partida, PartidaJugador

admin.site.register(Carta)
admin.site.register(Deck)
admin.site.register(Jugador)
admin.site.register(Partida)
admin.site.register(PartidaJugador)