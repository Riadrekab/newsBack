from django.contrib import admin
from .models import Profile, Category, Topic, Result

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Result)
