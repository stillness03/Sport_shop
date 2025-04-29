from django.db import models

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

class GymImage(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gyms/images/', blank=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.gym.name} - {self.image.name}"

    def get_amenities_list(self):
        return [a.strip() for a in self.amenities.split(',')]

    def __str__(self):
        return self.name