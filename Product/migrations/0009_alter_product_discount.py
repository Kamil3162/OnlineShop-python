# Generated by Django 3.2.16 on 2023-03-16 16:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0008_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(80)]),
        ),
    ]
