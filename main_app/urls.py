from django.urls import path

from . import views

urlpatterns = [
    path('get_average', views.get_average, name='get_average'),
    path('data_post', views.data_post, name='data_post'),
    path('filter_birthday', views.filter_birthday, name='filter_birthday'),
    path('upload_data_file', views.upload_data_file, name='upload_data_file'),
]
