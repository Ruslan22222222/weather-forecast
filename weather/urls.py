from django.urls import path
from weather.views import *

app_name = "weather"

urlpatterns = [
    path('', WeatherView.as_view(), name='search'),
    path('history/', HistoryView.as_view(), name='history'),
    path('api/history/', history_api, name='history_api'),
    path("autocomplete/", autocomplete_city, name="autocomplete"),
]
