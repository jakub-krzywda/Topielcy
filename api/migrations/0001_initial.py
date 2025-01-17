# Generated by Django 5.0.4 on 2024-04-18 23:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Users",
            fields=[
                ("userid", models.AutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=100)),
                ("email", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
                ("age", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="GPSData",
            fields=[
                ("dataid", models.AutoField(primary_key=True, serialize=False)),
                ("latitude", models.JSONField()),
                ("longitude", models.JSONField()),
                ("timestamps", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "userid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.users"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BioMedicalData",
            fields=[
                ("dataid", models.AutoField(primary_key=True, serialize=False)),
                ("pulse", models.JSONField()),
                ("timestamps", models.JSONField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "userid",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.users"
                    ),
                ),
            ],
        ),
    ]
