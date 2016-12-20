from django.contrib import admin

# Register your models here.
from .models import Restaurants
from .models import Preferences

admin.site.register(Restaurants)
admin.site.register(Preferences)