from django.contrib import admin
from .models import Person, PersonImage, Interest

# Register your models here.


admin.site.register(Person)
admin.site.register(PersonImage)
admin.site.register(Interest)
