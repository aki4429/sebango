from django.conf import settings
from django.db import models

class Shiire(models.Model):
    scode = models.CharField(max_length=30)
    sname = models.CharField(max_length=200)

    def __str__(self):
        return self.scode

class Bango(models.Model):
    hcode = models.CharField(max_length=200, null=True, blank=True)
    se = models.CharField(max_length=30, unique=True)
    shiire = models.ForeignKey(Shiire, on_delete=models.CASCADE, null=True, blank=True)
    kikaku = models.CharField(max_length=200, null=True, blank=True)
    biko = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.se

class Label(models.Model):
    sebango = models.ForeignKey(Bango, on_delete=models.CASCADE)
    qty = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.sebango
