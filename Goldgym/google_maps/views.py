import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Gym
import logging
logger = logging.getLogger(__name__)

def gym_detail_api(request, gym_id):
    try:
        gym = get_object_or_404(Gym, id=gym_id)
        logger.info(f"loading gtm: {gym.name}")
        logger.info(f"Time: {gym.opening_hours_weekdays} / {gym.opening_hours_saturday} / {gym.opening_hours_sunday}")
        ...
    except Exception as e:
        logger.exception("Erorr in loading gym_detail_api")
        return JsonResponse({'error': 'Internal server error'}, status=500)

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

    amenities_list = [
        "Aqua Classes", "Basketball Court", "Boxing", "Cardio Cinema®",
        "Cardio Equipment", "Chiropractic Services", "Circuit Training",
        "Cold Plunge", "Compression Therapy", "Coworking Space", "DEKA",
        "Free Weights", "Functional Training", "Gold's Burn®", "Gold's Fit®",
        "Group Cycle", "Group Exercise", "Gym80 Equipment", "Hyrox",
        "inBody Scanning", "Kid's Club", "LesMills Classes", "Locker Rooms",
        "Lounge Area", "Massage", "Mind & Body Studio", "Nutrition Counseling",
        "Olympic Lifting Platforms", "Outdoor Workout Area", "Percussion Therapy",
        "Personal Training", "Physical Therapy", "Pickleball", "Pilates", "Pool",
        "Posing Room", "Pro Shop", "Racquetball Courts", "Recovery Area",
        "Red Light Therapy", "Resistance Machines", "Sauna", "Small Group Training",
        "Smoothie Bar", "Spa", "Steam Room", "Strength Equipment", "Swim Lessons",
        "Tanning", "Tennis", "Towel Service", "Track", "Turf Area",
        "Wellness Services", "WiFi", "Women's Only Area"
    ]

    return render(request, 'google_maps/map.html', {'gyms': gyms, 'amenities_list': amenities_list})


def gym_detail_api(request, gym_id):
    try:
        gym = get_object_or_404(Gym, id=gym_id)

        additional_images = []
        if hasattr(gym, 'images'):
            additional_images = [img.image.url for img in gym.images.all() if img.image]

        data = {
            'id': gym.id,
            'name': gym.name,
            'address': gym.address,
            'latitude': gym.latitude,
            'longitude': gym.longitude,
            'amenities': gym.amenities.split(','),
            'opening_hours_weekdays': gym.opening_hours_weekdays,
            'opening_hours_saturday': gym.opening_hours_saturday,
            'opening_hours_sunday': gym.opening_hours_sunday,
            'phone': gym.phone,
            'email': gym.email,
            'image_url': gym.image.url if gym.image else None,
            'additional_images': additional_images,
            'is_open': is_gym_open(gym),
            'status': 'OPEN' if is_gym_open(gym) else 'CLOSED'
        }
        return JsonResponse(data)
    except Gym.DoesNotExist:
        return JsonResponse({'error': 'Gym not found'}, status=404)

def parse_hours(hours_str):
    if not hours_str:
        return None, None
    try:
        start_str, end_str = hours_str.split('-')
        try:
            start = datetime.datetime.strptime(start_str.strip(), "%I %p").time()
            end = datetime.datetime.strptime(end_str.strip(), "%I %p").time()
        except ValueError:
            start = datetime.datetime.strptime(start_str.strip(), "%I:%M %p").time()
            end = datetime.datetime.strptime(end_str.strip(), "%I:%M %p").time()
        return start, end
    except:
        return None, None


def is_gym_open(gym):
    now = datetime.datetime.now()
    current_time = now.time()
    weekday = now.weekday()

    if weekday < 5:
        hours = gym.opening_hours_weekdays
    elif weekday == 5:
        hours = gym.opening_hours_saturday
    else:
        hours = gym.opening_hours_sunday

    start, end = parse_hours(hours)
    if start and end:
        if start < end:
            return start <= current_time <= end
        else:
            return current_time >= start or current_time <= end
    return False