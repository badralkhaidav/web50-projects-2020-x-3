# Generated by Django 2.2.10 on 2020-06-20 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='topping',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]