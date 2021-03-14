from django.urls import path
from . import views

urlpatterns = [
    path('', views.BangoList.as_view(), name='bango_list'),
]