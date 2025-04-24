from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('all-media/', views.all_media, name='all_media'),
    path('upload/', views.upload_media, name='upload_media'),
    path('<int:pk>/', views.album_detail, name='album_detail'),
    path('assign/', views.assign_to_album, name='assign_to_album'),
]
