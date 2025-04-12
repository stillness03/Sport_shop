from django.contrib import admin
from .models import CalorieProfile


@admin.register(CalorieProfile)
class CalorieProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'weight', 'height', 'activity_level', 'goal', 'bmr', 'daily_calories', 'target_calories')
    list_filter = ('gender', 'activity_level', 'goal')
    search_fields = ('user__username',)