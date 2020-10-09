from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django import forms
from django.utils.text import Truncator

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Hidden

from .models import Event
from .forms import EventForm

# Create your views here.

class EventList(ListView):
    model = Event


class EventDetail(DetailView):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    model = Event


@login_required
@require_http_methods(['POST'])
def modify_registration(request, pk):
    event = Event.objects.get(pk=pk)
    registration_type = request.POST.get('type')
    user_already_registered = request.user in event.participants.all()

    if event.registration_start_datetime:
        if registration_type=='register' and not user_already_registered:
            response = event.modify_registration(registration_type, request.user)
        elif registration_type=='deregister' and user_already_registered:
            response = event.modify_registration(registration_type, request.user)
        else:
            return HttpResponse('Error' + registration_type)

    return HttpResponse('Success')


class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    cancel_url = reverse_lazy('events')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['max_occupancy_is_current_occupancy'].widget = forms.HiddenInput()
        return form

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.cancel_url)
        elif 'image_dim_reset' in request.POST:
            return HttpResponse(status=204)
        else:
            return super().post(request, *args, **kwargs)


class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    default_cancel_url = reverse_lazy('events')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper.layout[-1][0].append(HTML(
            '''<button name="delete" class="btn btn-danger" data-slug="{{ event.slug }}" data-title="{{ event.title }}" data-event-delete-url="{% url 'event_delete' event.slug %}" id="event_delete">Delete</button>'''
        ))
        form.helper.layout.append(Hidden(
            'next',
            '{% if request.META.HTTP_REFERER %}{{ request.META.HTTP_REFERER }}{% else %}{{ default_cancel_url }}{% endif %}'
        ))
        return form

    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return HttpResponseRedirect(request.POST.get('next', self.default_cancel_url))
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        context['default_cancel_url'] = self.default_cancel_url
        return context


@login_required
@require_http_methods(['POST'])
def delete_event(request, slug):
    event = Event.objects.get(slug=slug)
    event.delete()
    return HttpResponse(reverse_lazy('events'))


@login_required
@require_http_methods(['POST'])
def modify_descr_truncate_num(request, pk):
    event = Event.objects.get(pk=pk)
    event.modify_descr_truncate_num(int(request.POST.get('num')))
    return HttpResponse('Success')


@login_required
@require_http_methods(['POST'])
def modify_truncated_descr(request, pk):
    event = Event.objects.get(pk=pk)
    length = int(request.POST.get('num'))
    response = Truncator(event.description).words(length, html=True, truncate=' ...')
    return HttpResponse(response)

