# Generated by Django 4.1.2 on 2022-12-01 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepages', '0002_remove_food_food_group_remove_food_meal_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient_condition',
            name='date_diagnosed',
            field=models.DateField(blank=True, null=True),
        ),
    ]