from datetime import datetime

import requests
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from weather.models import SearchHistory


class WeatherView(View):
    template_name = "weather-config/search/search.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('''
                <div class="alert alert-error shadow-lg">
                    <span>❌ Пожалуйста, войдите в систему для поиска погоды.</span>
                </div>
            ''')

        city = request.POST.get("city")

        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_params = {"name": city, "count": 1, "language": "ru", "format": "json"}
        geo_response = requests.get(geocode_url, params=geo_params).json()

        if not geo_response.get("results"):
            return HttpResponse('''
                <div class="alert alert-error shadow-lg">
                    <span>❌ Город не найден. Попробуйте ещё раз.</span>
                </div>
            ''')

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]
        city_name = geo_response["results"][0]["name"]

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["temperature_2m_max", "temperature_2m_min", "windspeed_10m_max"],
            "timezone": "auto",
            "forecast_days": 3
        }

        history_entry, created = SearchHistory.objects.get_or_create(
            user=request.user,
            city=city_name
        )
        if created:
            history_entry.count = 1
        else:
            history_entry.count += 1
        history_entry.save()

        weather_response = requests.get(weather_url, params=weather_params).json()
        daily_weather = weather_response.get("daily", {})

        context = {
            "city": city_name,
            "forecast": [
                {
                    "date": datetime.strptime(daily_weather["time"][i], "%Y-%m-%d"),
                    "temp_max": daily_weather["temperature_2m_max"][i],
                    "temp_min": daily_weather["temperature_2m_min"][i],
                    "wind_speed": daily_weather["windspeed_10m_max"][i],
                }
                for i in range(3)
            ]
        }

        return render(request, "weather-config/partials/forecast_card.html", context)


class HistoryView(LoginRequiredMixin, ListView):
    model = SearchHistory
    template_name = "weather-config/partials/history_table.html"
    context_object_name = "history"
    paginate_by = 7

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user).order_by('-last_search')


@login_required
def history_api(request):
    data = SearchHistory.objects.filter(user=request.user).values('city', 'count')
    return JsonResponse(list(data), safe=False)


def autocomplete_city(request):
    term = request.GET.get("city", "")
    if not term:
        return HttpResponse("")

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": term, "count": 5, "language": "ru", "format": "json"}

    try:
        response = requests.get(geo_url, params=params)
        data = response.json().get("results", [])
    except:
        data = []

    html = ""
    for item in data:
        name = item["name"]
        country = item.get("country", "")
        full = f"{name}, {country}"
        html += f"""
        <li>
            <button 
                hx-get="#" 
                onclick="document.querySelector('input[name=city]').value = '{name}'; document.getElementById('suggestions').innerHTML = '';">
                {full}
            </button>
        </li>
        """

    return HttpResponse(html)
