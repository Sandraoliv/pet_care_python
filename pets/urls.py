from django.urls import path
from .views import PetView
from pets import views


urlpatterns = [
    path('pets/', PetView.as_view()),
]