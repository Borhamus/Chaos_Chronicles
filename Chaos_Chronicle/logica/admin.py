from django.contrib import admin
from .models import Carta, Jugador, Partida, PartidaJugador, Deck



admin.site.register(Jugador)
admin.site.register(Partida)
admin.site.register(PartidaJugador)
admin.site.register(Deck)

class CartaAdmin(admin.ModelAdmin):
    list_display = ('imagen_ver', 'Nombre')


admin.site.register(Carta, CartaAdmin)