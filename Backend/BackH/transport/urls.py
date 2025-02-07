from django.urls import path
from .views import journey_list

urlpatterns = [
    path('journeys/', journey_list, name='journey-list'),
]
