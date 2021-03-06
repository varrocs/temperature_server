import datastore
import pygal
from pygal.style import LightGreenStyle

def _create_labels(labels):
    return map(lambda d: d.strftime("%H:%M"), labels)

def update_chart(path):
    datapoints = datastore.last_n(30)
    if not datapoints:
        return
    datapoints = datapoints[::-1]
    times = [ p['date'] for p in datapoints ]
    temperatures = [ p['temperature'] for p in datapoints ]
    humidities = [ p['humidity'] for p in datapoints ]

    chart = pygal.Line(
        fill=True,
        style=LightGreenStyle,
        legend_at_bottom=True,
        spacing=10,
        height=400,
        range=[0.0, 100.0])
    chart.value_formatter = lambda x: "%.0f" % x
    chart.x_labels = _create_labels(times)
    chart.add('°C', temperatures)
    chart.add('%', humidities, secondary=True)
    chart.render_to_file(path)