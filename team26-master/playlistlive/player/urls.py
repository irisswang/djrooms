from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.sign_in, name='sign-in'),
    path('after-sign-in/', views.mainPage, name='after-sign-in'),
    path('DJRoom/', views.DJRoom, name='DJRoom'),
    path('search/', views.search, name="search"),
    path('queue/', views.queue, name="queue"),
    path('delete/', views.delete_room, name="delete"),
    url(r'^new/$', views.new_room, name='new_room'),
    path('profile/<str:requested_spotid>/',views.profile,name="profile")
]