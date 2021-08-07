from django.db import models
from deal.models import Deal
from django.db.models.aggregates import Sum


class Customer(models.Model):
    username = models.CharField(max_length=48, primary_key=True)
    spent_money = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ('-spent_money',)


class Top5(models.Model):
    username = models.CharField(max_length=48, primary_key=True)
    spent_money = models.PositiveBigIntegerField(default=0)
    gems = models.CharField(default='', max_length=512)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)
