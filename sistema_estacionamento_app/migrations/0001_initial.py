# Generated by Django 5.1.3 on 2024-12-01 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Precos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataInic', models.DateField()),
                ('dataFim', models.DateField()),
                ('valorPreco', models.FloatField()),
            ],
        ),
    ]