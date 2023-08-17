import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):

    app_id = 'e6186a9a1c5928498d18cea38bb1fe77'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id


    if(request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()
        if res.get('main'):
            city_info = {
                'city': city.name,
                'temp': res['main']['temp'],
                'icon': res['weather'][0]['icon'],
                'temp_max': res['main']['temp_max'],
                'temp_min': res['main']['temp_min'],
                'error': False,
            }
        else:
            city_info = {
                'city': city.name,
                'error': True,
            }

        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)