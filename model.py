from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
#import sqlite3
import json
import os

app = Flask(__name__)
script_path = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+script_path+'/dht_database3.db'
db = SQLAlchemy(app)


class DHTRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    humidity = db.Column(db.Float())
    temperature = db.Column(db.Float())
    wine_humidity = db.Column(db.Float())
    wine_temperature = db.Column(db.Float())
    date = db.Column(db.DateTime())

    def __init__(self, humidity, temperature, wine_humidity, wine_temperature, date):
        self.humidity = humidity
        self.temperature = temperature
	self.wine_humidity = wine_humidity
        self.wine_temperature = wine_temperature
        self.date = date

    def __repr__(self):
        return 'H:{0},T:{1},U:{2},V:{3},DateTime:{4}\n'.format(self.humidity, self.temperature, self.wine_humidity, self.wine_temperature, self.date)

    def to_dict(self):
        d = {}
        d["id"] = self.id
        d["humidity"] = self.humidity
        d["temperature"] = self.temperature
	d["wine_humidity"] = self.wine_humidity
        d["wine_temperature"] = self.wine_temperature
        d["date"] = str(self.date)
        return d

    def to_json(self):
        d = self.to_dict()
        #e = {key:val for key, val in d.items() if val > 0}
        return json.dumps(d)

try:
    DHTRecord.query.first()
    #DHTRecord.query.filter_by(wine_temperature=0).delete()
except sqlalchemy.exc.OperationalError as e:
    print app.config['SQLALCHEMY_DATABASE_URI']
    print("Error: {0}".format(e))
    db.create_all()
