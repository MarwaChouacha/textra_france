from django.db import models

# Create your models here.
class facture(models.Model):
    num=models.CharField(max_length=100)
    datefact=models.DateField(null=True)
    textfact=models.TextField(null=True)
    total=models.FloatField(default=0,null=True)
    tva=models.FloatField(default=0,null=True)
    details=models.TextField(null=True)
    compte=models.CharField(null=True)
    categ=models.CharField(null=True)
    path=models.TextField(null=True)
    