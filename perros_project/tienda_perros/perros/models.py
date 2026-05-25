from django.db import models

class Perro(models.Model):

    nombre = models.CharField(max_length=100)

    raza = models.CharField(max_length=100)

    edad = models.IntegerField()

    tamaño = models.CharField(max_length=50)

    peso = models.FloatField()

    color = models.CharField(max_length=50)

    vacunado = models.BooleanField(default=False)

    adoptado = models.BooleanField(default=False)

    energia = models.IntegerField()

    genero = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre