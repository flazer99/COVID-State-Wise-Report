import requests
import json
import csv
from flask import *

app = Flask(__name__)

def restructure(buff):
    data = [x.split(',') for x in buff.read().split('\n') if(len(x.split(',')) >= 2)]
    return data

def fetch_state():
    link = "https://api.covid19india.org/data.json"

    r = requests.get(url = link)
    data = r.json()

    y = json.loads(json.dumps(data['statewise']))
    print(type(y))

    details = list()
    for i in y:
        res = [i['state'], i['active'], i['deltaconfirmed'], i['deaths'],
               i['deltadeaths'], i['recovered'], i['deltarecovered'],
               i['confirmed'], i['lastupdatedtime']]
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
    delta_active = list()

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
        delta_active.append([time_, int(i['dailyconfirmed'])])

    #Prediction

    # Total Cases
    f = open('prediction-total-cases.csv','r')
    pred_total_cases = restructure(f)
    # print(res[1:])
    cal_ind = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May'
           ,'06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct'
           , '11':'Nov', '12':'Dec'}
    
    for i in pred_total_cases[1:]:
        i[0] = cal_ind[i[0].split('-')[1]] + " " + i[0].split('-')[2]
        i[1] = int(float(i[1]))  

    #Active Cases
    f = open('prediction-active-cases.csv','r')
    pred_active_cases = restructure(f)

    for i in pred_active_cases[1:]:
        i[0] = cal_ind[i[0].split('-')[1]] + " " + i[0].split('-')[2]
        i[1] = int(float(i[1])) 
        if(i[1]<0):
            i[1] = 0

    #Daily Confirmed
    f = open('prediction-daily-cases.csv','r')
    pred_daily_cases = restructure(f)
    # print(res[1:])

    for i in pred_daily_cases[1:]:
        i[0] = cal_ind[i[0].split('-')[1]] + " " + i[0].split('-')[2]
        i[1] = int(float(i[1]))
        if(i[1]<0):
            i[1] = 0        
    return total_cases, total_deaths, total_recovered, total_active, daily_cases, daily_deaths, daily_recovered, pred_active_cases, pred_daily_cases, pred_total_cases, delta_active

def fetch_resources():
    link = "https://api.covid19india.org/resources/resources.json"

    r = requests.get(url = link)
    data = r.json()

    y = json.loads(json.dumps(data))
    resources = dict()
    for i in y['resources']:
        if(i['state'] not in resources):
            tmp = [[i['category'], i['city'], i['contact'], 
                    i['descriptionandorserviceprovided'], i['nameoftheorganisation']
                    ,i['phonenumber'], i['recordid'], i['state']]]
            resources[i['state']] = tmp

        else:
            resources[i['state']].append([i['category'], i['city'], i['contact'], 
                    i['descriptionandorserviceprovided'], i['nameoftheorganisation']
                    ,i['phonenumber'], i['recordid'], i['state']])
    return resources

@app.route("/")
def display_nation():
    total_cases, total_deaths, total_recovered, total_active, daily_cases, daily_deaths, daily_recovered, pred_active_cases, pred_daily_cases, pred_total_cases, delta_active = fetch_nation()
    return render_template('covid-main-nation.html', cases = total_cases[-1][1] , recovered = daily_recovered[-1]
    , deaths = daily_deaths[-1], confirmed = daily_cases[-1], total_cases = total_cases
    , total_recovered = total_recovered, total_deaths = total_deaths
    , total_active = total_active, delta_confirmed = delta_active, pred_total_cases = pred_total_cases[1:]
    , pred_active_cases = pred_active_cases[1:], pred_daily_cases = pred_daily_cases[1:])

@app.route("/state-wise")
def display_state():
    details = fetch_state()
    return render_template('covid-main-state.html', data = details)

@app.route("/contact")
def contact():
    return render_template('covid-main-contact.html')

@app.route("/resources")
def resources():
    resources = fetch_resources()
    return render_template('covid-main-resources.html', state = resources.keys(), ctr = 0, data = list(), select = "")

@app.route("/resources/select", methods = ["get"])
def resources_select():
    state = request.args.get('state')
    resources = fetch_resources()
    return render_template('covid-main-resources.html', state = resources.keys(), ctr = 1, data = resources[state], select = state)

if(__name__ == '__main__'):
    app.run(port = 8051, debug = True)
