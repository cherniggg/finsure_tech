from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
class Lender(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=3)
    upfront_commission_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MaxValueValidator(100), MinValueValidator(0)])
    trial_commission_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MaxValueValidator(100), MinValueValidator(0)])
    active = models.BooleanField()