from django.urls import path
from . import views

urlpatterns = [
    path('', views.BangoList.as_view(), name='bango_list'),
    path('label_list/', views.LabelList.as_view(), name='label_list'),
    path('label_delete_all/', views.label_delete_all, name='label_delete_all'),
    path('<int:pk>/update/', views.LabelUpdate.as_view(), name='label_edit'),
    path('make_label/', views.make_label, name='make_label'),
    path('upload/', views.upload, name='upload'),
    path('down_se/', views.down_sebango, name='down_se'),
    path('<int:pk>/detail/', views.BangoDetail.as_view(), name='bango_detail'),
    path('<int:pk>/bango_update/', views.BangoUpdate.as_view(), name='bango_update'),
    path('<int:pk>/bango_copy/', views.BangoCopy.as_view(), name='bango_copy'),
    path('<int:pk>/bango_delete/', views.BangoDelete.as_view(), name='bango_delete'),
]
