from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import mark_safe

class Carta(models.Model):
    Nombre = models.CharField(max_length=15)
    Ataque = models.SmallIntegerField()
    Defensa = models.SmallIntegerField()
    Costo = models.SmallIntegerField()
    Imagen = models.ImageField(blank=True, upload_to='cartas/')
   

    def __str__(self):
        return self.Imagen.url
    
    def imagen_ver(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.Imagen.url)

# TODO: Agregar en un atributo, todas las cartas.
class Deck(models.Model):
    Titulo = models.CharField(max_length=50)
    CantidadCartas = models.IntegerField(default=0, validators=[MinValueValidator(9), MaxValueValidator(21)])
    CantCirculo = models.SmallIntegerField(default=0)
    CantCuadrado = models.SmallIntegerField(default=0)
    CantTriangulo = models.SmallIntegerField(default=0)
    PartidasGanadas = models.SmallIntegerField(default=0)
    PartidasPerdidas = models.SmallIntegerField(default=0)
    PartidasTotales = models.SmallIntegerField(default=0)
    Winrate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    FechaDeCreacion = models.DateField(auto_now_add=True)
    BackImage = models.ImageField(blank=True, upload_to='backim/')
    Puntos = models.IntegerField(default=100)

    def calcular_winrate(self):
        total_partidas = self.PartidasTotales
        if total_partidas == 0:
            return 0
        partidas_ganadas = self.PartidasGanadas
        return (partidas_ganadas / total_partidas) * 100

    def save(self, *args, **kwargs):
        self.Winrate = self.calcular_winrate()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Titulo

    def get_absolute_url(self):
        return reverse('deck_detail', args=[str(self.id)])

    def contar_cartas_por_tipo(self):
        self.CantCirculo = self.deckcard_set.filter(tipo='ci').count()
        self.CantCuadrado = self.deckcard_set.filter(tipo='cu').count()
        self.CantTriangulo = self.deckcard_set.filter(tipo='tr').count()
        self.CantidadCartas = self.deckcard_set.count()
        self.Puntos = 100 - sum(self.deckcard_set.values_list('carta__Costo', flat=True))
        self.save()

    def validar(self):
        if (self.CantidadCartas > 21 or self.CantidadCartas < 9):
            return (False)
        elif (self.Puntos < 0):
            return (False)
        else: return (True)

class DeckCard(models.Model):
    TIPO_CHOICES = [
        ('ci', 'Circulo'),
        ('cu', 'Cuadrado'),
        ('tr', 'Triangulo'),
    ]

    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    imagenTipo = models.ImageField(blank=True, upload_to='tipes/')


#    def __str__(self):
#        return "{}_{}".format(self.deck.__str__(), self.carta.__str__())
    def __str__(self):
        return f"{self.carta.Nombre} ({self.get_tipo_display()}) en {self.deck.Titulo}"

class Jugador(AbstractUser):
    ScoreTotal = models.SmallIntegerField(default=0)
    PartidasGanadas = models.IntegerField(default=0)
    PartidasPerdidas = models.IntegerField(default=0)
    Decks = models.ManyToManyField(Deck, blank=True)
    FotoPerfil = models.ImageField(blank=True, upload_to='perfilimages/')
    deck_seleccionado = models.ForeignKey('Deck', on_delete=models.SET_NULL, null=True, blank=True, related_name='jugador_seleccionado')

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.pk})

#Función para clonar un Deck
def clonar_deck(deck):
    # Crear una copia del deck
    nuevo_deck = Deck.objects.create(
        Titulo=f"{deck.Titulo} (Incial)",
        CantidadCartas=deck.CantidadCartas,
        CantCirculo=deck.CantCirculo,
        CantCuadrado=deck.CantCuadrado,
        CantTriangulo=deck.CantTriangulo,
        PartidasGanadas=deck.PartidasGanadas,
        PartidasPerdidas=deck.PartidasPerdidas,
        PartidasTotales=deck.PartidasTotales,
        Winrate=deck.Winrate,
        BackImage=deck.BackImage,
        Puntos=deck.Puntos
    )
    # Copiar las cartas asociadas al deck
    for deck_card in deck.deckcard_set.all():
        DeckCard.objects.create(
            deck=nuevo_deck,
            carta=deck_card.carta,
            tipo=deck_card.tipo,
            imagenTipo=deck_card.imagenTipo
        )
    return nuevo_deck

# Señal para asignar automáticamente un deck clonado a cada jugador nuevo
@receiver(post_save, sender=Jugador)
def asignar_deck_predeterminado(sender, instance, created, **kwargs):
    if created:  # Solo funciona cuando un jugador nuevo es creado
        deck_predeterminado = Deck.objects.first()  # Obtén el primer deck en la base de datos
        if deck_predeterminado:
            nuevo_deck = clonar_deck(deck_predeterminado)  # Crear una copia del deck
            instance.Decks.add(nuevo_deck)  # Asignar el deck clonado al jugador
            instance.deck_seleccionado = nuevo_deck  # Asignar el deck clonado como el deck seleccionado
            instance.save()

class Partida(models.Model):
    Fecha = models.DateField(auto_now_add=True)
    TiempoJugado = models.DurationField()
    members = models.ManyToManyField(Jugador, through="PartidaJugador")

    def __str__(self):
        return f'Partida {self.Fecha}'

class PartidaJugador(models.Model):
    Jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    Deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    Partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    GanadorPerdedor = models.BooleanField()
    ScoreGanado = models.SmallIntegerField()

    def __str__(self):
        return f'{self.Jugador.username} en {self.Partida}'
    
    def save(self, *args, **kwargs):
        if not self.Deck and self.Jugador.deck_seleccionado:
            self.Deck = self.Jugador.deck_seleccionado

        # Determina si esta es una instancia nueva
        is_new = self.pk is None

        # Guarda la instancia de PartidaJugador
        super().save(*args, **kwargs)

        # Actualiza el ScoreTotal del jugador
        self.Jugador.ScoreTotal += self.ScoreGanado

        # Si es una instancia nueva, actualiza las partidas ganadas o perdidas
        if is_new:
            if self.GanadorPerdedor:
                self.Jugador.PartidasGanadas += 1
            else:
                self.Jugador.PartidasPerdidas += 1

        self.Jugador.save()