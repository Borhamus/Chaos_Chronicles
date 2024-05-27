from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import render
from django.db import models
from django.urls import reverse

class Carta(models.Model):
    Nombre = models.CharField(max_length=15)
    Ataque = models.SmallIntegerField()
    Defensa = models.SmallIntegerField()
    Costo = models.SmallIntegerField()
    Imagen = models.ImageField(blank=True, upload_to='cartas/')
    imagenTipo = models.ImageField(blank=True, upload_to='tipes/')

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
    CantCirculo = models.SmallIntegerField()
    CantCuadrado = models.SmallIntegerField()
    CantTriangulo = models.SmallIntegerField()
    PartidasGanadas = models.SmallIntegerField()
    PartidasPerdidas = models.SmallIntegerField()
    PartidasTotales = models.SmallIntegerField()
    Winrate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    FechaDeCreacion = models.DateField(auto_now_add=True)
    Cartas = models.ManyToManyField(Carta, blank=True)
    BackImage = models.ImageField(blank=True, upload_to='backimages/')

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
    ScoreTotal = models.SmallIntegerField(default=0)
    Decks = models.ManyToManyField(Deck, blank=True)
    FotoPerfil = models.ImageField(blank=True, upload_to='perfilimages/')

    def __str__(self):
        return self.username

class Partida(models.Model):
    Fecha = models.DateField(auto_now_add=True)
    TiempoJugado = models.TimeField(auto_now=False, auto_now_add=False)
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

def partida_list(request):
    partidas = Partida.objects.all()
    return render(request, 'partida_list.html', {'partidas': partidas})

def partida_create(request):
    if request.method == 'POST':
        # Lógica para crear una nueva partida
        pass
    return render(request, 'partida_form.html')