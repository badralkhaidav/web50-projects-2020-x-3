# Generated by Django 2.2.10 on 2020-06-20 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0002_product_topping'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(default='', max_length=64),
        ),
    ]
