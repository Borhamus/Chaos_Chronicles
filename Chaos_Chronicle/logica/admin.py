from django.contrib import admin
from .models import Carta, Jugador, Partida, PartidaJugador

admin.site.register(Carta)
admin.site.register(Jugador)
admin.site.register(Partida)
admin.site.register(PartidaJugador)