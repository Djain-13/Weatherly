import os
from flask import Flask, render_template, request
from weather_app import main as get_weather
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None 
    graph_path = None

    
    if request.method == 'POST':
        city = request.form['CityName']
        country = request.form['CountryName']
        data, graph_path = get_weather(city, country) 

        if graph_path and os.path.exists(graph_path):
            os.remove(graph_path)
        os.rename('forecast_graph.png', graph_path)

    return render_template('index.html', data=data, graph_path=graph_path)

if __name__=='__main__':
    app.run(debug=True)