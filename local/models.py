from django.db import models
from django_mysql.models import ListTextField


# Create your models here.
# class SearchedValues(models.Model):
#     searchlist = models.CharField(max_length=100)
#     mileagerange = models.CharField(max_length=100)
#     pricerange = models.CharField(max_length=100)
#
#     def __str__(self):
#         return f"{self.searchlist} {self.mileagerange} {self.pricerange}"

class SearchedValue(models.Model):
    searchlist = ListTextField(base_field=models.CharField(max_length=100), size=100)
    mileagerange = ListTextField(base_field=models.CharField(max_length=100), size=100)
    pricerange = ListTextField(base_field=models.CharField(max_length=100), size=100)
    yearmodel = ListTextField(base_field=models.CharField(max_length=100), size=100)

    def __str__(self):
        return f"{self.searchlist} {self.mileagerange} {self.pricerange}"
