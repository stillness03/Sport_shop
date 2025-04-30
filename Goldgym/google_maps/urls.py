from django.urls import path
from . import views
from .views import gym_detail_api

urlpatterns = [
    path('gyms/', views.gym_locator, name='google_maps'),
    path('gym-detail/<int:gym_id>/', gym_detail_api, name='gym_detail_api'),
]