# Generated by Django 3.2.16 on 2023-02-20 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Product', '0004_alter_shipaddress_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('Complain', 'Reklamacja'), ('Return', 'Zwrot - 14 dni'), ('Ship', 'Gdzie moja paczka?'), ('Defect', 'Wada fabryczna')], default=('Complain', 'Reklamacja'), max_length=20)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
