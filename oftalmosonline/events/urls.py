from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('<slug>/', views.EventDetailView.as_view(), name='event-detail'),
    path('<slug>/update/', views.EventUpdateView.as_view(), name='event-update'),
    path('<slug>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
   

]