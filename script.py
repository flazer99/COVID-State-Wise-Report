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
    f = open('covid-data-statewise.csv', 'r')
    res = restructure(f)

    return render_template('covid-main.html', data = res[2:])



if(__name__ == '__main__'):
    link = "https://api.covid19india.org/data.json"

    r = requests.get(url = link)
    data = r.json()

    y = json.loads(json.dumps(data['statewise']))
    print(type(y))

    filename = './covid-data-statewise.csv'
    with open(filename, 'w') as f: 
        w = csv.DictWriter(f,['active','confirmed',
        'deaths','deltaconfirmed','deltadeaths',
        'deltarecovered','lastupdatedtime','recovered'
        ,'state','statecode','statenotes']) 
        w.writeheader() 
        for i in y: 
            w.writerow(i) 

    app.run(port = 8051, debug = True)
