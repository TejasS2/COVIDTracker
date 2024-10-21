from typing import Any
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import datetime
from .forms import UserForm
from django.http import HttpResponse
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.db.models import Q
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
import subprocess
import html

from .models import Country, Data, User

# Create your views here
def home(request):
    return render(request, "countries/home.html")

# Countries
class CountryViewList(ListView):
    model = Country
    template_name = 'countries/country_list.html'
    context_object_name = 'countries'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Country.objects.filter(Q(name__icontains=query))
        else:
            return Country.objects.all()

class CountryDetailView(DetailView):
    model = Country
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country = self.get_object()
        
        decoded_country_name = html.unescape(country.name)

        country_name_for_url = decoded_country_name.replace(" ", "+")
        google_maps_embed_url = f"https://www.google.com/maps?q={country_name_for_url}&output=embed"
        dates = Data.objects.filter(country=country).order_by('-date').values_list('date', flat=True).distinct()
        
        context['google_maps_embed_url'] = google_maps_embed_url
        context['dates'] = dates
        return context

class CountryDateDetailView(DetailView):
    model = Country
    template_name = "countries/country_date_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country = self.get_object()
        date_str = self.kwargs.get('date')
        
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            data_for_date = Data.objects.get(country=country, date=date_obj)
        except (ValueError, Data.DoesNotExist):
            return HttpResponseRedirect(reverse('countries:country_detail'))


        context['data_for_date'] = data_for_date
        return context

def fetch_countries(request):
    if request.method == 'POST':
        try:
            result = subprocess.run(['python', 'initialize.py'], check=True)
            if result.returncode == 0:
                messages.success(request, 'Countries successfully fetched and updated.')
        except subprocess.CalledProcessError:
            messages.error(request, 'There was an error fetching countries. Try a different API key.')
        return HttpResponseRedirect(reverse('countries:country_list'))

    return HttpResponseRedirect(reverse('home'))

def fetch_data(request, country_id):
    try:
        country = Country.objects.get(pk=country_id)
    except Country.DoesNotExist:
        return HttpResponseRedirect(reverse('countries:country_list'))

    if request.method == 'POST':
        selected_date = request.POST.get('fetch_date')
        try:
            result = subprocess.run(['python', 'initialize.py', country.name, selected_date], check=True)
            if result.returncode == 0:
                messages.success(request, 'Data successfully fetched and updated.')
        except subprocess.CalledProcessError:
            messages.error(request, 'No data found for the selected date.')
        return HttpResponseRedirect(reverse('countries:country_detail', args=[country_id]))

    return HttpResponseRedirect(reverse('countries:country_detail', args=[country_id]))

# Users
class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'countries/user_form.html'
    success_url = reverse_lazy('countries:country_list')
    
def info(request):
    return render(request, "countries/info.html")
