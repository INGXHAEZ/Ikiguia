from django.contrib import admin

from django.contrib import admin
from .models import Carrera
from .models import Mentor

admin.site.register(Carrera)
admin.site.register(Mentor)