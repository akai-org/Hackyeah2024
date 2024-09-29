from django.db import models

# Create your models here.
class Code2TaxPlace(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)


class Voievodeship(models.Model):
    name = models.CharField(max_length=100)
    on_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Powiat(models.Model):
    name = models.CharField(max_length=100)
    voievodeship = models.ForeignKey(Voievodeship, on_delete=models.CASCADE)
    on_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Gmina(models.Model):
    name = models.CharField(max_length=100)
    powiat = models.ForeignKey(Powiat, on_delete=models.CASCADE)
    on_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)