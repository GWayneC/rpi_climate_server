import time
from datetime import datetime
import Adafruit_DHT as Sensor
import threading
from model import db, DHTRecord
from optparse import OptionParser
from generate_graph import generate_graph

sensor_args = { '11': Sensor.DHT11, '22': Sensor.DHT22, '2302': Sensor.AM2302}

def add_parser_options(parser):
    parser.add_option('-p', action="store_true", default=False, help="print every record to STDOUT [default: %default]")
    parser.add_option('-t', action="store", type="int", default=5, help="time interval in minutes to request readout from sensor [default: %default]")
    parser.add_option('--pin', dest="pin", action="store", type="int", default=4, help="data pin connected to sensor [default: %default]")
    parser.add_option('-s', action="store", type="str", default='11', help="number of DHT sensor in use (supported: 11, 22, 2302) [default: %default]")
    return parser


class SensorDatabase(threading.Thread):
    def __init__(self, pin, sensor_number, minutes_interval, print_to_stdout):
        self.pin = pin
        self.sensor_number = sensor_number
        self.minutes_interval = 5 #minutes_interval
        self.print_to_stdout = True #print_to_stdout
        threading.Thread.__init__(self)

    def record_to_database(self, data):
        humidity, temperature, wine_humidity, wine_temperature, datetime = data
        record = DHTRecord(humidity, temperature, wine_humidity, wine_temperature, datetime)
        print(record)
        db.session.add(record)
        db.session.commit()
        generate_graph()

    def run(self):
        while True:
           print('Getting room temperature and humidity')
           humidity, temperature = Sensor.read_retry(self.sensor_number, 17)
           print('Humidity is {0:0.1f} %').format(humidity)
           print('Temperature is {0:0.1f} C').format(temperature)
           print('Getting wine room temperature and humidity') 
           wine_humidity, wine_temperature = Sensor.read_retry(self.sensor_number, self.pin)
           print('Humidity is {0:0.1f} %').format(wine_humidity)
           print('Temperature is {0} C').format(wine_temperature)
 
           if temperature == 0:
               temperature_F = 0
           else:
               temperature_F = (temperature * 9/5) + 32
           if wine_temperature == 0:
               wine_temperature_F = 0
           else:
               wine_temperature_F = (wine_temperature * 9/5) + 32
            
           data = humidity, temperature_F, wine_humidity, wine_temperature_F, datetime.now()
           print(data)
           self.record_to_database(data)
           one_minute = 60
           sleep_time = self.minutes_interval * one_minute
           if self.print_to_stdout:
               print(data)
           time.sleep(sleep_time)

if __name__ == "__main__":
    parser = OptionParser()
    praser = add_parser_options(parser)
    opts, args = parser.parse_args()
    sensor = sensor_args[opts.s]
    sd = SensorDatabase(opts.pin, sensor, opts.t, opts.p)
    sd.run()
