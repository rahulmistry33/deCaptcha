from django.urls import path
from . import views

urlpatterns = [	
    path('index/',views.index, name='index'),
    path('crack/',views.crack, name='crack'),
    path('crackImage/',views.crackImage, name='crackImage'),
]