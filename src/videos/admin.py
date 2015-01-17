from django.contrib import admin

# Register your models here.
from .models import Video, Category


admin.site.register(Video)

admin.site.register(Category)