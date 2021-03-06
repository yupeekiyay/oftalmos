from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Event
from django.views import generic
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from .forms import EventModelForm
from django.shortcuts import redirect
from oftalmosonline.users.models import UserCalendar, User
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

class LandingPageView(generic.TemplateView):
    template_name = '../templates/userevents.html'

    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect("user_events")
        return super().dispatch(request,*args,**kwargs)


class EventListView(generic.ListView):
    template_name = "discover_events.html"
    

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(EventListView, self).get_context_data(**kwargs)
        thirty_days_ago=datetime.date.today()+datetime.timedelta(days=7)
        next_in_thirty=Event.objects.filter(user=user, event_date_start__gt=datetime.date.today(),event_date_start__lt=thirty_days_ago)
        past_events=Event.objects.filter(user=user, event_date_finish__lt=datetime.date.today())
        recently_added = Event.objects.filter(created=datetime.date.today()).count()
        context.update({
                  "next_in_thirty":next_in_thirty, 
                  "past_events":past_events, 
                  "recently_added":recently_added,            
         })
        
        return context

    def get_queryset(self):
        queryset = Event.objects.filter(global_visibility=True, event_date_start__gte=datetime.date.today())
        return queryset
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):

        if self.request.method == 'POST':
            post_id = request.POST['post_id']
            user = User.objects.get(id=request.user.id)   
            event = Event.objects.get(id=post_id)
            user.usercalendar.events.add(event.id)
            
            print(user.usercalendar.events)
            return HttpResponse() # Sending an success response
        else:
            return HttpResponse("Request method is not a POST")

    
class EventDetailView(generic.DetailView):
    template_name = "events/event.html"
    queryset = Event.objects.all()
    context_object_name = "event"

    # def get_context_data(self, **kwargs):
    #     context = super(EventDetailView, self).get_context_data(**kwargs)
    #     product = self.get_object()
    #     has_access = False
    #     if self.request.user.is_authenticated:
    #         if product in self.request.user.userlibrary.products.all():
    #             has_access = True
    #     context.update({
    #         "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
    #         "has_access": has_access
    #     })
    #     return context

class UserEventListView(LoginRequiredMixin,  generic.ListView):
    template_name = "userevents.html"
    

    def get_queryset(self):
        user = self.request.user
        
        queryset = UserCalendar.objects.filter(user=user, events__event_date_start__gte=datetime.date.today())
        
        return queryset
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        print(user)
        context = super(UserEventListView, self).get_context_data(**kwargs)
        
        past_events=UserCalendar.objects.filter(user=user, events__event_date_finish__lt=datetime.date.today())
        context.update({
                  "past_events":past_events, 
         })
       
        return context

class EventCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "events/event_create.html"
    form_class = EventModelForm

    def get_success_url(self):
        return reverse("events:event-detail", kwargs={
            "slug":self.event.slug
        })
    
    def form_valid(self,form):
        # need to change for admin - admin's changes are in normal status 
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        self.event = instance
        return super(EventCreateView, self).form_valid(form)

class EventUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "events/event_update.html"
    
    form_class = EventModelForm

    def get_success_url(self):
        return reverse('user_events')
    # def get_success_url(self):
    #     return reverse("events:event-detail", kwargs={
    #         "slug":self.get_object().slug
    #     })
    
    def get_queryset(self):
        return Event.objects.filter(user = self.request.user)

    def form_valid(self,form):
        user=self.request.user
        if user.is_superuser:
            return super(EventUpdateView, self).form_valid(form) 
        else:
            instance = form.save(commit=False)
            instance.global_visibility = False
            instance.save()
        
        return super(EventUpdateView, self).form_valid(form)    


class EventDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "events/event_delete.html"
    
    form_class = EventModelForm

    def get_success_url(self):
        return reverse('user_events')
    
    def get_queryset(self):
        return Event.objects.filter(user = self.request.user)




