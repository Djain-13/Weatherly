import os
from flask import Flask, render_template, request
from weather_app import main as get_weather
import datetime

app = Flask(__name__)

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None 
    graph_url = None
    if request.method == 'POST':
        city = request.form['CityName']
        country = request.form['CountryName']
        data, temp_graph_path = get_weather(city, country)

        if temp_graph_path:
            graph_filename = 'forecast_graph.png'
            graph_path = os.path.join(STATIC_DIR, graph_filename)
            os.rename(temp_graph_path, graph_path)
            graph_url = f'/static/{graph_filename}'
        
    return render_template('index.html', data=data, graph_url=graph_url)

if __name__=='__main__':
    app.run(debug=True)