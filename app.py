from flask import Flask, render_template, request
from weather_app import main as get_weather
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None 
    if request.method == 'POST':
        city = request.form['CityName']
        country = request.form['CountryName']
        data = get_weather(city, country) 
    return render_template('index.html', data=data)

if __name__=='__main__':
    app.run(debug=True)