from django.contrib import admin

from apps.events.models import Category, Event


admin.site.register(Event)
admin.site.register(Category)
