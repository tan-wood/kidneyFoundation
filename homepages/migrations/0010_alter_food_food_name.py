# Generated by Django 4.1.2 on 2022-12-02 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepages', '0009_alter_alert_type_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='food_name',
            field=models.CharField(max_length=150),
        ),
    ]
