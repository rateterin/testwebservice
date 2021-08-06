from django.db import models
from django.utils import timezone


class Deal(models.Model):
    customer = models.ForeignKey(to='customer.Customer', to_field='username', on_delete=models.CASCADE)
    item = models.CharField(max_length=24, blank=False, null=False)
    total = models.PositiveBigIntegerField(default=0, blank=False, null=False)
    quantity = models.PositiveIntegerField(default=0, blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)


class ImportLog(models.Model):
    file = models.FileField(upload_to='deals')
    date = models.DateTimeField(auto_now=True)
    success = models.BooleanField(default=False)
