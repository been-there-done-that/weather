from django.shortcuts import render
import requests
from . import (models,forms)

def index(request):
    cities = models.City.objects.all() #return all the cities in the database

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=c834efb84c6315bba71d237277828930'

    if request.method == 'POST': # only true if form is submitted
        # breakpoint()
        form = forms.CityForm(request.POST) # add actual request data to form for processing
        if not models.City.objects.filter(name=request.POST.get('name')).exists():
            form.save() # will validate and save if validate

    form = forms.CityForm()

    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
        # breakpoint()
        if city_weather['cod'] == '404':
            continue
        else:
            weather = {
                'city' : city,
                'temperature' : city_weather['main']['temp'],
                'description' : city_weather['weather'][0]['description'],
                'icon' : city_weather['weather'][0]['icon']
            }

        weather_data.append(weather) #add the data for the current city into our list
    
    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context) #returns the index.html template