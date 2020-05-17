import requests
import json
import csv
from flask import *

app = Flask(__name__)

def fetch():
    link = "https://api.covid19india.org/data.json"

    r = requests.get(url = link)
    data = r.json()

    y = json.loads(json.dumps(data['statewise']))
    print(type(y))

    details = list()
    for i in y:
        res = [i['state'], i['active'], i['deaths'], i['recovered'], i['confirmed'], i['lastupdatedtime']]
        details.append(res)
    return details

@app.route("/")
def display():
    details = fetch()
    return render_template('covid-main.html', data = details)


if(__name__ == '__main__'):
    app.run(port = 8051, debug = True)
