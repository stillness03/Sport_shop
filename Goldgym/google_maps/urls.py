from django.urls import path
from . import views

urlpatterns = [
    path('gyms/', views.gym_locator, name='google_maps'),
]