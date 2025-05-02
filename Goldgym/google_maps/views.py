from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Gym
from .utils import is_gym_open

# Added only to check errors
import logging
logger = logging.getLogger(__name__)


def gym_detail_api(request, gym_id):
    try:
        gym = get_object_or_404(Gym, id=gym_id)
        logger.info(f"Loading gym: {gym.name}")
        logger.info(
            f"Time: {gym.opening_hours_weekdays} / {gym.opening_hours_saturday} / {gym.opening_hours_sunday}")
        ...
    except Exception as e:
        logger.exception("Error in louding gym_detail_api")
        return JsonResponse({'error': 'Internal server error'}, status=500)
# /


def gym_locator(request):
    gyms = []
    for gym in Gym.objects.all():
        is_open = is_gym_open(gym)
        gyms.append({
            'id': gym.id,
            'name': gym.name,
            'latitude': gym.latitude,
            'longitude': gym.longitude,
            'address': gym.address,
            'is_open': is_open,
            'status': 'OPEN' if is_open else 'CLOSED',
        })
    return render(request, 'google_maps/map.html', {'gyms': gyms})


def gym_detail_api(request, gym_id):
    try:
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
            'image_url': gym.image.url if gym.image else None,
            'is_open': is_gym_open(gym),
            'status': 'OPEN' if is_gym_open(gym) else 'CLOSED',
        }
        return JsonResponse(data)
    except Gym.DoesNotExist:
        return JsonResponse({'error': 'Gym not found'}, status=404)
