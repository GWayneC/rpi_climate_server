import sqlite3
import plotly
from plotly.graph_objs import Scatter, Layout, Figure


def generate_graph():
    conn = sqlite3.connect('dht_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * from dht_record')
    database_list = cursor.fetchall()
    conn.close()

    humidity_list = [round(i[1],1) for i in database_list]
    temperature_list = [round(i[2],1) for i in database_list]
    date_list = [i[3] for i in database_list]

    temperature_F_list = [round((i * (9.0/5.0)) + 32, 1) for i in temperature_list]


    #temperature_trace = Scatter(x=date_list, y=temperature_list, name='Temperature (C)')
    temperature_F_trace = Scatter(x=date_list, y=temperature_F_list, name='Temperature (F)')
    humidity_trace = Scatter(x=date_list, y=humidity_list, name='Humidity (%)', yaxis='Date')

    data = [temperature_F_trace, humidity_trace]


    layout = Layout(title='Home Temperature and Humidity', yaxis=dict(title='Humidity (%), Temperature (F)'))


    fig = Figure(data=data, layout=layout)
    plot_url = plotly.offline.plot(fig, filename='templates/climate_graph.html', auto_open=False)



generate_graph()