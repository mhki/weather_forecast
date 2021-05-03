import requests
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import City
from .model import UserCity
from . import db

main = Blueprint('main', __name__)

def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={ city }&units=metric&APPID=d6548e7d52c7b86e0ae8327f327dd426'
    r = requests.get(url).json()
    return r


@main.route('/')
def index_get():
    return redirect(url_for('auth.login'))

#Hail Mary  
@main.route('/profile')
@login_required
def profile():
    #Cities The Users Add
    user_cities= UserCity.query.all()
    #Cities Added By the admin aka popular cities
    cities = City.query.all()

    weather_data1 = []

    weather_data = []

    #Current User Home City
    e = get_weather_data(current_user.home)
    weather_user = {
            'city' : current_user.home,
            'country' : e['sys']['country'],
            'temperature' : e['main']['temp'],
            'description' : e['weather'][0]['description'],
            'icon' : e['weather'][0]['icon'],
    }

    
    for city in cities:

        z = get_weather_data(city.home)
        
        weather = {
            'city' : city.home,
            'country' : z['sys']['country'],
            'temperature' : z['main']['temp'],
            'description' : z['weather'][0]['description'],
            'icon' : z['weather'][0]['icon'],
        }

        weather_data1.append(weather)

    for city in user_cities:
        if current_user.id == city.author_id:
            r = get_weather_data(city.home)
            
            weather = {
                'city' : city.home,
                'country' : r['sys']['country'],
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }

            weather_data.append(weather)

    return render_template('profile.html',weather_data1=weather_data1,   weather_data = weather_data,weather_user=weather_user, username=current_user.username, home=current_user.home)

@main.route('/profile', methods=['POST'])
@login_required
def profile_post():
    err_msg =''
    new_city = request.form.get('city')

    if new_city:
        existing_city = UserCity.query.filter_by(home=new_city).first()
        if not existing_city:
            new_city_data = get_weather_data(new_city)

            if new_city_data['cod'] == 200:
                new_city_obj = UserCity(home=new_city, author_id=current_user.id)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                err_msg = 'City does not exist in the world'
        else:
            err_msg = 'City Already Exists in The Database!'

    if err_msg:
        flash(err_msg)
    else:
        flash('City Added Succesfully!')
    
    return redirect(url_for('main.profile'))

@main.route('/delete/<name>')
def delete_city(name):
    city = UserCity.query.filter_by(home=name).first()
    db.session.delete(city)
    db.session.commit()

    flash(f'Successfully deleted { city.home }', 'success')
    return redirect(url_for('main.profile'))



