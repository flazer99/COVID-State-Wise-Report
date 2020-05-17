import requests
import json
import csv
from flask import *

app = Flask(__name__)

def restructure(buff):
    data = [x.split(',') for x in buff.read().split('\n') if(len(x.split(',')) >= 2)]
    return data

@app.route("/")
def display():
    return render_template('covid-main.html', data = details)


if(__name__ == '__main__'):
    link = "https://api.covid19india.org/data.json"

    r = requests.get(url = link)
    data = r.json()

    y = json.loads(json.dumps(data['statewise']))
    print(type(y))

    details = list()
    for i in y:
        res = [i['state'], i['active'], i['deaths'], i['recovered'], i['confirmed'], i['lastupdatedtime']]
        details.append(res)

    app.run(port = 8051, debug = True)
