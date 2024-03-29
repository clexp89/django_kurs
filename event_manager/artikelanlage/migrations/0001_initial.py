# Generated by Django 5.0.3 on 2024-03-12 13:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Konto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nummer', models.PositiveIntegerField(max_length=7, unique=True)),
                ('bezeichnung', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Lieferant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nummer', models.PositiveIntegerField(unique=True)),
                ('bezeichnung_1', models.CharField(max_length=40)),
                ('bezeichnung_2', models.CharField(blank=True, max_length=40, null=True)),
                ('gruppe', models.CharField(choices=[('elektro', 'Elektro'), ('stahl', 'Stahl'), ('hydraulik', 'Hydraulik')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artikel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nummer', models.CharField(blank=True, max_length=8, null=True)),
                ('mengeneinheit', models.CharField(choices=[('KG', 'Kg'), ('M', 'Meter'), ('stk.', 'Stueck')], max_length=8)),
                ('bezeichnung_1', models.CharField(max_length=40)),
                ('bezeichnung_2', models.CharField(blank=True, max_length=40, null=True)),
                ('lieferant_artikel_nr', models.CharField(blank=True, max_length=40, null=True)),
                ('zeichnungs_nummer', models.CharField(blank=True, max_length=20, null=True)),
                ('gewicht', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('ist_angelegt', models.BooleanField(default=False)),
                ('anforderungsdatum', models.DateField()),
                ('anforderer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('konto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artikelanlage.konto')),
                ('lieferant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='artikelanlage.lieferant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
