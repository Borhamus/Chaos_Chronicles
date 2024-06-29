from django.contrib import admin
from .models import Carta, Jugador, Partida, PartidaJugador, Deck

class CartaAdmin(admin.ModelAdmin):
    list_display = ('imagen_ver', 'Nombre')

class PartidaJugadorInline(admin.TabularInline):
    model = PartidaJugador
    extra = 1  # Número de forms extra

class PartidaAdmin(admin.ModelAdmin):
    list_display = ('Fecha', 'TiempoJugado')
    inlines = [PartidaJugadorInline]

admin.site.register(Jugador)
admin.site.register(PartidaJugador)
admin.site.register(Deck)
admin.site.register(Partida, PartidaAdmin)
admin.site.register(Carta, CartaAdmin)