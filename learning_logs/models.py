from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


class Topic(models.Model):
    """Тема, яку вивчає користувач"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Повернути рядкове представлення моделі"""
        return self.text


class Entry(models.Model):
    """Якась конкретна інформація до цієї теми"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = RichTextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    entry_name = models.CharField(max_length=200)

    # https://django-taggit.readthedocs.io/en/latest/api.html#TaggableManager
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Povernut ryadkove predstavlennya modeli"""
        if len(self.text) <= 50:
            return f"{self.text}"
        else:
            return f"{self.text[:50]}..."
