# Generated by Django 3.1.7 on 2021-08-25 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10)),
                ('extra', models.CharField(blank=True, max_length=64)),
                ('primary', models.ManyToManyField(related_name='primarySymptom', to='checker.Symptom')),
                ('secondary', models.ManyToManyField(blank=True, related_name='secondarySymptom', to='checker.Symptom')),
            ],
        ),
    ]
