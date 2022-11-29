from django.db import models
from datetime import datetime, timedelta

# # Create your models here.


class Food(models.Model):
    food_name = models.CharField(max_length=50)
    
    def __str__(self):
        return (self.description)


# class TripCategory(models.Model):
#     description = models.CharField(max_length=20)

#     # this is basically just so that if you ever try to grab the 
#     # 'TripCategory' object as a whole it will return what it is and
#     # not some random code you won't understand
#     def __str__(self):
#         return (self.description)

# class Destination(models.Model):
#     # CASCADE deletes all the linked records if that record is deleted
#     trip_category = models.OneToOneField(TripCategory, on_delete=models.CASCADE)
#     title = models.CharField(max_length=50)
#     days = models.IntegerField(default=0)
#     cost = models.DecimalField(max_digits=8, decimal_places=2)
#     main_photo = models.ImageField(upload_to='photos')
#     is_active = models.BooleanField(default=True)
#     leave_data = models.DateField(default=datetime.today, blank=True)

#     def __str__(self):
#         return(self.title)

# class Customer(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     user_name = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#     email = models.EmailField(max_length=100)
#     phone = models.CharField(max_length=13, blank=True)
#     destinations = models.ManyToManyField(Destination, blank=True)

#     def __str__(self) :
#         return (self.full_name)

#     @property
#     def full_name(self) :
#         return '%s %s' % (self.first_name, self.last_name)

#     def save(self) :
#         self.first_name = self.first_name.upper()
#         self.last_name = self.last_name.upper()
#         super(Customer, self).save()







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


# class Alert(models.Model) :
#     date_time = models.DateTimeField()
#     alert_type = models.