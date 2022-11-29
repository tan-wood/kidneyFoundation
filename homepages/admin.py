from django.contrib import admin

from .models import Nutrient, MealCategory, FoodGroup, Food, Measurement, Nutrient_In_Food, Patient, Patient_Logs_Food, Condition, Patient_Condition, Diet, Alert, Alert_Type

# Register your models here.
admin.site.register(Nutrient)
admin.site.register(MealCategory)
admin.site.register(FoodGroup)
admin.site.register(Food)
admin.site.register(Measurement)
admin.site.register(Nutrient_In_Food)
admin.site.register(Patient)
admin.site.register(Patient_Condition)
admin.site.register(Patient_Logs_Food)
admin.site.register(Condition)
admin.site.register(Diet)
admin.site.register(Alert)
admin.site.register(Alert_Type)


