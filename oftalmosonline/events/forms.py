from django import forms
from .models import Event


class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'title',
            'tags',
            'cover',
            'description',
            'organizer',
            'event_format',
            'main_language',
            'event_url',
            'event_date_start',
            'event_time_start',
            'event_date_finish',
            'event_time_finish',
            'is_cme',
        )
