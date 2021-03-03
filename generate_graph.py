import sqlite3
import plotly
from plotly.graph_objs import Scatter, Layout, Figure


def generate_graph():
    conn = sqlite3.connect('dht_database3.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * from dht_record where  wine_humidity > 0') 
    database_list = cursor.fetchall()
    conn.close()


    humidity_list = [i[1] for i in database_list]
    temperature_list = [i[2] for i in database_list]
    wine_humidity_list = [i[3] for i in database_list]
    wine_temperature_list = [i[4] for i in database_list]
    date_list = [i[5] for i in database_list]

    #temperature_F_list = [round((i * (9.0/5.0)) + 32, 1) for i in temperature_list]
    #wine_temperature_F_list = [round((i * (9.0/5.0)) + 32, 1) for i in temperature_list]

    #temperature_trace = Scatter(x=date_list, y=temperature_list, name='Temperature (C)')
    temperature_trace = Scatter(x=date_list, y=temperature_list, name='Temperature (F)')
    wine_temperature_trace = Scatter(x=date_list, y=wine_temperature_list, name='Wine Temperature (F)')
    humidity_trace = Scatter(x=date_list, y=humidity_list, name='Humidity (%)')
    wine_humidity_trace = Scatter(x=date_list, y=wine_humidity_list, name='Wine Humidity (%)')

    data = [temperature_trace, humidity_trace,wine_temperature_trace, wine_humidity_trace]

    layout = Layout(title='Wine Room Temperature and Humidity', yaxis=dict(title='Humidity (%), Temperature (F)'))


    fig = Figure(data=data, layout=layout)
    print('generating graph with : {0}'.format(data))
    fig.write_html("templates/index.html")
    #plot_url = plotly.offline.plot(fig, filename='templates/climate_graph.html', auto_open=False)



#generate_graph()
