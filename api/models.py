from django.db import models


# Create your models here.
class Users(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BioMedicalData(models.Model):
    dataid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='biomedical_data')
    pulse = models.JSONField()
    timestamps = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


class GPSData(models.Model):
    dataid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='gps_data')
    latitude = models.JSONField()
    longitude = models.JSONField()
    timestamps = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
