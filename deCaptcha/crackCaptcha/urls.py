from django.urls import path
from . import views

urlpatterns = [	
    path('index/',views.index, name='index'),
    path('home/', views.home, name ='home'),
    path('crack/',views.crack, name='crack'),
    path('generate/',views.generate, name='generate'),
    path('crackImage/',views.crackImage, name='crackImage'),
]