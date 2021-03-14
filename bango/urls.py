from django.urls import path
from . import views

urlpatterns = [
    path('', views.BangoList.as_view(), name='bango_list'),
    path('label_list/', views.LabelList.as_view(), name='label_list'),
    path('label_delete_all/', views.label_delete_all, name='label_delete_all'),
    path('<int:pk>/update/', views.LabelUpdate.as_view(), name='label_edit'),
    path('make_label/', views.make_label, name='make_label'),
]
