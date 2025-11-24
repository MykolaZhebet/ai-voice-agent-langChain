from django.urls import path
from . import views
urlpatterns = [
    path('chat/', views.home_page, name='home_page')
]