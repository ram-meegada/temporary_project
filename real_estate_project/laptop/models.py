from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


# Create your models here.
class LaptopModel(models.Model):
    name = models.CharField(max_length=100)
    link_subscription = models.URLField(("Insight URL"), max_length=100, blank=True, null=True)
    link_subsc = models.URLField(("Insight URL"), max_length=100, blank=True, null=True)



# print(3410000000/800000000, '------eps-------')	
# print(4.2625 * 49.2)

# class CustomExceptionType(Exception):
#     pass

# try:
#     raise CustomExceptionType('This is for testing...........')
# except Exception as err:
#     print(err)
#     print(type(err).__name__)




# from django.utils import timezone


# t = timezone(2025, 1, 1)
# print(t)


class FloatDecimalModel(models.Model):
    f = models.FloatField()
    d = models.DecimalField(max_digits=10, decimal_places=4)



class Amodel(models.Model):
    name = models.CharField(max_length=100)

class Bmodel(models.Model):
    name = models.CharField(max_length=100)

class Cmodel(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now(), blank=True, null=True)
