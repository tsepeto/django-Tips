from django.db import models
from django.utils import timezone
import datetime
from django.urls import reverse

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=256)
    parts = models.IntegerField()

    def get_absolute_url(self):
        return reverse('employee_list')

    def __str__(self):
        return self.name

class Posto(models.Model):
    name = models.CharField(max_length=256)

    def get_absolute_url(self):
        return reverse('posto_list')

    def __str__(self):
        return self.name


class Tip(models.Model):
    posto = models.ForeignKey('diaxoristis.Posto',related_name = 'tips',on_delete = 'CASCADE')
    start_date =models.DateField()
    end_date = models.DateField()
    money = models.FloatField()

    def get_absolute_url(self):
        return reverse('tip_list')

    def __str__(self):
        formatedDate = self.start_date.strftime("%d-%m-%Y")
        return str(formatedDate)
