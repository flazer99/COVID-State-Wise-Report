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
    f = open('covid-data-district.csv', 'r')
    res = restructure(f)

    return render_template('test.html', data = res[1:])



if(__name__ == '__main__'):
    link = "https://api.covid19india.org/state_district_wise.json"

    r = requests.get(url = link)
    data = r.json()

    y = json.loads(json.dumps(data['Andhra Pradesh']))

    districts = list()
    for i in y['districtData']:
        data = dict()
        data['districtName'] = i
        data['activeCases'] = y['districtData'][i]['active']
        data['deaths'] = y['districtData'][i]['deceased']
        data['recovered'] = y['districtData'][i]['recovered']
        data['confirmed'] = y['districtData'][i]['confirmed']
        districts.append(data)

    filename = './covid-data-district.csv'
    with open(filename, 'w') as f: 
        w = csv.DictWriter(f,['districtName','activeCases',
        'deaths','recovered','confirmed']) 
        w.writeheader() 
        for i in districts: 
            w.writerow(i) 

    app.run(port = 8051, debug = True)

