from django.contrib import admin
from .models import Gym, GymImage

@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
     list_display = ('name', 'address')
     search_fields = ('name', 'address')

class GymImageInline(admin.TabularInline):
    model = GymImage
    extra = 1