from django.contrib import admin
from .models import Profile, Category, Topic, Result, historyResult, Preference

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Topic)
admin.site.register(Result)
admin.site.register(historyResult)
admin.site.register(Preference)
