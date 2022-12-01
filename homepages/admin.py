from django.contrib import admin

from .models import Nutrient, Food, Measurement, Nutrient_In_Food, Patient, Patient_Logs_Food, Condition, Patient_Condition, Diet, Alert, Alert_Type, Patient_Favorite_Food

# Register your models here.
admin.site.register(Nutrient)
admin.site.register(Food)
admin.site.register(Measurement)
admin.site.register(Nutrient_In_Food)
admin.site.register(Patient)
admin.site.register(Patient_Favorite_Food)
admin.site.register(Patient_Condition)
admin.site.register(Patient_Logs_Food)
admin.site.register(Condition)
admin.site.register(Diet)
admin.site.register(Alert)
admin.site.register(Alert_Type)


