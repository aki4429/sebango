from django.shortcuts import render
from .models import Bango, Shiire
from django.views.generic import ListView
 
 
class BangoList(ListView):
    template_name='bango/bango_list.html'
    context_object_name = 'bango_list'
    model = Bango 
