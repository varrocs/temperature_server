import datastore
import pygal

def update_chart(path):
    datapoints = datastore.last_n(30)
    times = [ p['date'] for p in datapoints ]
    temperatures = [ p['temperature'] for p in datapoints ]
    humidities = [ p['humidity'] for p in datapoints ]

    chart = pygal.Line()
    chart.x_labels=times
    chart.add('Temperature', temperatures)
    chart.add('Humidity', humidities)
    chart.render_to_file(path)