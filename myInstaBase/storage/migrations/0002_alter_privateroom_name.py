# Generated by Django 4.0.5 on 2022-06-19 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privateroom',
            name='name',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
