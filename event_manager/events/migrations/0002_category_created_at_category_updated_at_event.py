# Generated by Django 5.0.3 on 2024-03-11 10:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('sub_title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(help_text='Beschreibung des Events')),
                ('date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('min_group', models.PositiveSmallIntegerField(choices=[(2, 'kleine Gruppe'), (5, 'mittelgroße Gruppe'), (10, 'große Gruppe'), (0, 'keine Begrenzung')])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
