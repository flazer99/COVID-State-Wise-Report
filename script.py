import requests
import json
import csv
from flask import *

app = Flask(__name__)

def fetch_state():
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

def fetch_nation():
    link = "https://api.covid19india.org/data.json"

    r = requests.get(url = link)
    data = r.json()
    
    z = json.loads(json.dumps(data['cases_time_series']))
    nation_details = list()
    
    total_cases = list()
    total_deaths = list()
    total_recovered = list()
    total_active = list()

    daily_cases = list()
    daily_deaths = list()
    daily_recovered = list()

    cal = {'January':'Jan', 'February':'Feb', 'March':'Mar', 'April':'Apr', 'May':'May'
           ,'June':'Jun', 'July':'Jul', 'August':'Aug', 'September':'Sep', 'October':'Oct'
           , 'November':'Nov', 'December':'Dec'}
    for i in z:
        res = [i['dailyconfirmed'], i['dailydeceased'], i['dailyrecovered'], i['date'], i['totalconfirmed']
        , i['totaldeceased'], i['totalrecovered']]
        nation_details.append(res)
        date, month = i['date'].split()
        month = cal[month]
        time_ = str(month) + " " + str(int(date))
        
        daily_cases.append(i['dailyconfirmed'])
        daily_deaths.append(i['dailydeceased'])
        daily_recovered.append(i['dailyrecovered'])
        
        total_cases.append([time_, int(i['totalconfirmed'])])
        total_deaths.append([time_, int(i['totaldeceased'])])
        total_recovered.append([time_, int(i['totalrecovered'])])
        total_active.append([time_, int(i['totalconfirmed'])-int(i['totaldeceased'])-int(i['totalrecovered'])])
        
    return total_cases, total_deaths, total_recovered, total_active, daily_cases, daily_deaths, daily_recovered

@app.route("/")
def display_nation():
    total_cases, total_deaths, total_recovered, total_active, daily_cases, daily_deaths, daily_recovered = fetch_nation()
    return render_template('covid-main-nation.html', active = total_active[-1][1] , recovered = daily_recovered[-1]
    , deaths = daily_deaths[-1], confirmed = daily_cases[-1], total_cases = total_cases
    , total_recovered = total_recovered, total_deaths = total_deaths
    , total_active = total_active)

@app.route("/state-wise")
def display_state():
    details = fetch_state()
    return render_template('covid-main-state.html', data = details)

@app.route("/contact")
def contact():
    return render_template('covid-main-contact.html')
    
if(__name__ == '__main__'):
    app.run(port = 8051, debug = True)
