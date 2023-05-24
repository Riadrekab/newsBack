from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')

    def __str__(self):
        return self.name


class Profile(models.Model):
    WORK_CHOICES = [
        ('1', 'Yes'),
        ('0', 'No'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=600, null=True, blank=True)
    work = models.CharField(max_length=1, choices=WORK_CHOICES, null=True, blank=True)
    at_work_from = models.TimeField(null=True, blank=True)
    at_work_to = models.TimeField(null=True, blank=True)
    preferred_topics = models.ManyToManyField(Topic, related_name='preferred_topics', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.work == '1':
            if self.at_work_from is None or self.at_work_to is None:
                raise ValidationError('Please provide work hours')
            if self.at_work_from > self.at_work_to:
                raise ValidationError('Work from time should be less than work to time')
        else:
            self.at_work_from = None
            self.at_work_to = None
        return super().clean()

    def __str__(self):
        return str(self.user.username)


class historyResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    input = models.CharField(max_length=250, null=True, blank=True)


class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=600, null=True, blank=True)
    image = models.CharField(max_length=250, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['profile', 'title']

    def __str__(self):
        return str(self.title)


class Preference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    see_at_work = models.BooleanField(default=False)
    see_at_weekend = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['profile', 'category']

    def __str__(self):
        return str(self.category.name)
