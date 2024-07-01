from django.contrib import admin
from .models import Carta, Jugador, Partida, PartidaJugador, Deck
from django.utils.html import mark_safe

class CartaAdmin(admin.ModelAdmin):
    list_display = ('imagen_ver', 'Nombre')

class PartidaJugadorAdmin(admin.ModelAdmin):
    list_display = ('Jugador','ScoreGanado', 'Partida', 'Deck', 'ganadorperdedor')
    def ganadorperdedor(self, obj):
        if obj.GanadorPerdedor:
            return 'Ganador'
        else:
            return 'Perdio'

class PartidaJugadorInline(admin.TabularInline):
    model = PartidaJugador
    extra = 1  # Número de forms extra

class PartidaAdmin(admin.ModelAdmin):
    list_display = ('Fecha', 'TiempoJugado', 'allmembers')
    inlines = [PartidaJugadorInline]
    def allmembers(self, obj):
        return ', '.join([Jugador.username for Jugador in obj.members.all()])

class JugadorAdmin(admin.ModelAdmin):
    list_display = ('username', 'deck_seleccionado', 'image' )
    def image(self, obj):
        if obj.FotoPerfil:
            return mark_safe('<img src="{0}" width="75" height="75" />'.format(obj.FotoPerfil.url))
        else:
            return ''
        
class DeckAdmin(admin.ModelAdmin):
    list_display = ('Titulo', 'CantidadCartas', 'image' )
    def image(self, obj):
        if obj.BackImage:
            return mark_safe('<img src="{0}" width="75" height="75" />'.format(obj.BackImage.url))
        else:
            return ''

admin.site.register(Jugador, JugadorAdmin)
admin.site.register(PartidaJugador, PartidaJugadorAdmin)
admin.site.register(Deck, DeckAdmin)
admin.site.register(Partida, PartidaAdmin)
admin.site.register(Carta, CartaAdmin)