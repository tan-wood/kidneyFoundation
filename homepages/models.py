from django.db import models
from datetime import datetime, timedelta

# Create your models here.



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

class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    weight = models.FloatField(default=0)
    height = models.FloatField(default=0)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=13, blank=True)
    address1 = models.CharField(max_length=20)
    address2 = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=9)

    class Meta:
        db_table = "patient"

    def __str__(self) :
        return (self.full_name)
    
    @property
    def full_name(self) :
        return '%s %s' % (self.first_name, self.last_name)

    def save(self) :
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        super(Patient, self).save()

class Patient_Logs_Food (models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0.0)
    class Meta:
        db_table = "patient_logs_food"

class Condition(models.Model) :
    description = models.CharField(max_length=25)
    patients = models.ManyToManyField(Patient, through='Patient_Condition', blank=True)

    class Meta:
        db_table = "condition"

class Patient_Condition(models.Model) :
    class Meta :
        db_table = 'patient_condtion'
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    date_diagnosed = models.DateField()

class Diet(models.Model) :
    description = models.CharField(max_length=25)
    patients = models.ManyToManyField(Patient, blank=False)
    class Meta :
        db_table = "diet"


class Alert_Type(models.Model) :
    description = models.CharField(max_length=25)

    class Meta :
        db_table = 'patient_condtion'


class Alert(models.Model) :
    date_time = models.DateTimeField()
    alert_type = models.ForeignKey(Alert_Type, null=False, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, null=False, on_delete=models.CASCADE)

    class Meta :
        db_table = 'patient_condtion'

