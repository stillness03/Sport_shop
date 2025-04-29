from django.shortcuts import render
from Goldgym import secret
from .models import Gym

def gym_locator(request):
    gyms = Gym.objects.all()
    for gym in gyms:
        gym.amenities_list = gym.amenities.split(',')
    return render(request, 'google_maps/map.html', {
        'gyms': gyms,
        'google_maps_key': secret.google_api_key
    })




