from django.contrib import admin
from .models import Tag, Agenda, Entity, Category, Faculty, Event


class EventAdmin(admin.ModelAdmin):
    list_display = ['title','slug','category','description', 'created',
                    'global_visibility','event_format','main_language','event_date_start','event_date_finish','is_cme']

    search_fields=['title','slug','category','global_visibility','event_format','main_language','event_date_start','is_cme']

class TagAdmin(admin.ModelAdmin):
    list_display = ['tag']

class AgendaAdmin(admin.ModelAdmin):
    list_display=['time_start', 'topic','faculty','event' ]

class FacultyAdmin(admin.ModelAdmin):
    list_display=['prefix', 'first_name',  'last_name']
    search_fields=[ 'first_name',  'last_name']

class CategoryAdmin(admin.ModelAdmin):
    list_display=['topic']
    search_fields=['topic']

class EntityAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Event, EventAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Agenda,AgendaAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Entity, EntityAdmin)