from django.db import models
from django.db.models.fields import NullBooleanField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from common.utils.text import unique_slug
from django.urls import reverse
from django.contrib.auth import get_user_model




class Category(models.Model):
    TOPIC_CHOICES = [('cataract', 'Cataract'),
                     ('vitreo', 'Vitreoretinal'),
                     ('optometry', 'Optometry'),
                     ('multi', 'Multidisciplinary'),
                     ('plastic', 'Plastic and Reconstructive surgery'),
                     ('onco', 'Ocular oncology'),
                     ('glaucoma', 'Glaucoma'),
                     ('pediatrics', 'Pediatrics'), ]
    topic = models.CharField(max_length=100, choices=TOPIC_CHOICES)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.topic

class Tag(models.Model):
    tag = models.CharField(max_length=50)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['tag']
    
    def __str__(self):
        return self.tag

class Entity(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name_plural = "Entities"
    def __str__(self):
        return self.name

class Faculty(models.Model):
    prefix = models.CharField(max_length=5, default="Mr")
    first_name = models.CharField(max_length=50, blank=True,null=True)
    last_name = models.CharField(max_length=100)
    event = models.ManyToManyField("Event")
    class Meta:
        verbose_name_plural = "Faculty"
    def __str__(self):
        return f"{self.prefix} {self.first_name} {self.last_name}"

class Agenda(models.Model):
    time_start = models.TimeField(null=True, blank=True)
    topic = models.CharField(max_length=250, null=True, blank=True)
    faculty=models.ForeignKey(Faculty, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey("Event",blank=True, null=True, on_delete=models.SET_NULL)
    class Meta:
        verbose_name_plural = "Agenda"
    def __str__(self):
        return f"{self.time_start} {self.topic} {self.faculty}"


class Event(models.Model):
    LANGUAGE_CHOICES = [
        ('EN', 'English'), ('IT', 'Italian'), ('FR', 'French'), ('DE', 'German'), ('RU', 'Russian'), ]
    STATUS_CHOICES = [('draft', 'Draft'), ('confirmed', 'Confirmed'), ]
    FORMAT_CHOICES = [('live', 'Live'), ('online', 'Online'), ]
    # VISIB_CHOICES = [('personal', 'Personal'),('moderation','Moderation'),('global','Global')]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=50,unique=True, editable=False, null=False)
    tags = models.ManyToManyField('Tag', blank=True)
    
    category = models.ForeignKey(Category,null=True,  on_delete=models.SET_NULL)
    cover = models.ImageField(blank=True,null=True, upload_to="event_covers/")
    

    description = models.TextField(blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    organizer = models.ForeignKey(Entity, blank=True, null=True, on_delete=models.SET_NULL)
    # visibility = models.CharField(
    #     max_length=100, choices=VISIB_CHOICES, default='personal')
    global_visibility = models.BooleanField(default=True)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default='draft')
    event_format = models.CharField(
        max_length=50, choices=FORMAT_CHOICES, default='online')
    main_language = models.CharField(
        max_length=50, choices=LANGUAGE_CHOICES, default='EN')
    event_url = models.URLField(blank=True)
    event_date_start = models.DateField()
    event_time_start = models.TimeField(default='09:00')
    event_date_finish = models.DateField()
    event_time_finish = models.TimeField(default='18:00')
    is_cme = models.BooleanField(
        default=False, verbose_name='CME credits', db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            value=str(self)
            self.slug = unique_slug(value, type(self))
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("events:event-detail", kwargs={
            "slug":self.slug
        })
    
    def get_update_url(self):
        return reverse('events:event-update', kwargs={
            "slug": self.slug
        })
    def get_delete_url(self):
        return reverse('events:event-delete', kwargs={
            "slug": self.slug
        })
    
class UserEvents(models.Model):
    pass