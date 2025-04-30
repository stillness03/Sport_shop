from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Gym

def gym_locator(request):
    gyms = Gym.objects.all()
    for gym in gyms:
        gym.amenities_list = gym.amenities.split(',')
    return render(request, 'google_maps/map.html', {
        'gyms': gyms,
    })

def gym_detail_api(request, gym_id):
    gym = get_object_or_404(Gym, id=gym_id)
    data = {
        'id': gym.id,
        'name': gym.name,
        'address': gym.address,
        'amenities': gym.amenities.split(','),
        'opening_hours_weekdays': gym.opening_hours_weekdays,
        'opening_hours_saturday': gym.opening_hours_saturday,
        'opening_hours_sunday': gym.opening_hours_sunday,
        'phone': gym.phone,
        'email': gym.email,
        'image_url': gym.image.url if gym.image else None
    }
    return JsonResponse(data)


