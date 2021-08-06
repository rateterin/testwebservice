from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=48, primary_key=True)
    spent_money = models.PositiveBigIntegerField(default=0)


class Top5(models.Model):
    username = models.CharField(max_length=48, primary_key=True)
    spent_money = models.PositiveBigIntegerField(default=0)
    gems = models.CharField(default='', max_length=512)
