from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from oftalmosonline.events.models import Event
from django.views.decorators.csrf import csrf_exempt
class User(AbstractUser):
    """Default user for OftalmosOnline."""

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

class UserCalendar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event, blank=True)
    

    def __str__(self):
        return self.user.username  

    


def post_save_user_receiver(sender, instance, created,**kwargs):
    if created:
        calendar=UserCalendar.objects.create(user=instance)
        calendar.events.add(id=0)
        instance.save()


post_save.connect(post_save_user_receiver, sender=User)
