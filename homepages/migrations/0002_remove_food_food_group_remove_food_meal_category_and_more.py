# Generated by Django 4.1.2 on 2022-12-01 16:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='food_group',
        ),
        migrations.RemoveField(
            model_name='food',
            name='meal_category',
        ),
        migrations.AddField(
            model_name='patient_logs_food',
            name='date_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='condition',
            name='patients',
            field=models.ManyToManyField(through='homepages.Patient_Condition', to='homepages.patient'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address2',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='patient_condition',
            name='date_diagnosed',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.DeleteModel(
            name='FoodGroup',
        ),
        migrations.DeleteModel(
            name='MealCategory',
        ),
    ]
