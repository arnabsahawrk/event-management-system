from django.contrib import admin

from apps.events.models import Category, Event, Participant


admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Participant)
