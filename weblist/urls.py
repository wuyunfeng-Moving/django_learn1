from django.urls import path
from . import views

urlpatterns = [
    path('linkinput/', views.linkinput, name='linkinput'),
    path('linkdisplay/', views.linkdisplay, name='linkdisplay'),
    path('savetext/', views.savetext, name='savetext'),
    path('youtube/', views.youtube, name='youtube'),
    path('youtubelist/',views.youtubelist,name='youtubelist'),
]
