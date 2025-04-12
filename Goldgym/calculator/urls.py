from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.calorie_calculator, name='calculator'),
    path('result/', views.result, name='result'),
]