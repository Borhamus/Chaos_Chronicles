from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import render
from .models import Partida, PartidaJugador

class Carta(models.Model):
    Nombre = models.CharField(max_length=15)
    Ataque = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    Defensa = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    Costo = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(999)])
    Imagen = models.ImageField(blank=True, upload_to='pendiente/')
    imagenTipo = models.ImageField(blank=True, upload_to='pendiente/')

    TIPO_CHOICE = (
        ('tr', 'Triangulo'),
        ('cu', 'Cuadrado'),
        ('ci', 'Circulo'),
    )

    Tipo = models.CharField(max_length=2, choices=TIPO_CHOICE, blank=True)

    def __str__(self):
        return self.Nombre

class Deck(models.Model):
    Titulo = models.CharField(max_length=50)
    CantidadCartas = models.IntegerField(default=0, validators=[MinValueValidator(9), MaxValueValidator(21)])
    CantCirculo = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    CantCuadrado = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    CantTriangulo = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    PartidasGanadas = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    PartidasPerdidas = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    PartidasTotales = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    Winrate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    FechaDeCreacion = models.DateField(auto_now_add=True)
    Cartas = models.ManyToManyField(Carta, blank=True)
    BackImage = models.ImageField(blank=True, upload_to='pendiente/')

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

class Jugador(AbstractUser):
    ScoreTotal = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(999999)])
    Decks = models.ManyToManyField(Deck, blank=True)
    FotoPerfil = models.ImageField(blank=True, upload_to='pendiente/')

    def __str__(self):
        return self.username

class Partida(models.Model):
    Fecha = models.DateField(auto_now_add=True)
    TiempoJugado = models.TimeField(auto_now=False, auto_now_add=False)
    members = models.ManyToManyField(
        Jugador,
        through="PartidaJugador",
    )

    def __str__(self):
        return f'Partida {self.Fecha}'

class PartidaJugador(models.Model):
    Jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    Deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    Partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    GanadorPerdedor = models.BooleanField()
    VidaRestante = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    ScoreGanado = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])

    def __str__(self):
        return f'{self.Jugador.username} en {self.Partida}'

def partida_list(request):
    partidas = Partida.objects.all()
    return render(request, 'partida_list.html', {'partidas': partidas})

def partida_create(request):
    if request.method == 'POST':
        # Lógica para crear una nueva partida
        pass
    return render(request, 'partida_form.html')