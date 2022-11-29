from tkinter import CASCADE
from django.db import models
from datetime import datetime, timedelta

# # Create your models here.



class Nutrient(models.Model):
    nutrients_macro = models.BooleanField
    nutrient_name = models.CharField(max_length=50)

    def __str__(self):
        return (self.nutrient_name)
    
    class Meta:
        db_table = "nutrient"

class Food(models.Model):
    food_name = models.CharField(max_length=50)
    nutrient = models.ManyToManyField(Nutrient, through='Nutrient_In_Food', blank=False)

    def __str__(self):
        return (self.food_name)
    
    class Meta:
        db_table = "food"


class Measurement(models.Model):
    description = models.CharField(max_length=50)

    def __str__(self):
        return (self.description)
    
    class Meta:
        db_table = "measurement"


class Nutrient_In_Food(models.Model):
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    amount = models.FloatField(null=False, blank=False, default=0.0)
    class Meta:
        db_table = "nutrient_in_food"


