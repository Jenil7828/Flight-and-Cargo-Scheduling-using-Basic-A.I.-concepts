from django.contrib import admin
from .models import Flight, Cargo

# Register your models here.
admin.site.register(Flight)
admin.site.register(Cargo)
