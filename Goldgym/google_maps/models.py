from django.db import models
from .utils import is_gym_open


class Gym(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()
    opening_hours_weekdays = models.CharField(max_length=255, null=True, blank=True)
    opening_hours_saturday = models.CharField(max_length=255, null=True, blank=True)
    opening_hours_sunday = models.CharField(max_length=255, null=True, blank=True)
    amenities = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to='gyms/', null=True, blank=True)

    def get_amenities_list(self):
        return [a.strip() for a in self.amenities.split(',')]

    def is_gym_open(self):
        return is_gym_open(self)


class GymImage(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gyms/images/', blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.gym.name}"