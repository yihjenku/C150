from flask import Flask, render_template, request
import requests
from translators import search as s, Graphics as g

app = Flask(__name__)
app.config['DEBUG'] = True  # Disable this for deployment

@app.route('/', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':

        maxwatt = []
        fortymin = []
        onemin = []
        twentymin = []
        repmax = []

        Tests = {'Max Watt': maxwatt, 'Twenty Minute': twentymin, 'One Minute': onemin, \
            'Forty Minute': fortymin, 'Rep Max': repmax}

        name = request.form['user_search'].lower().title()
        rower_data = s.searchRower(name)
        if rower_data['items']:
            g.graphOlympic(name)
            g.graphSplitChanges(name)

        for rower in rower_data['items']:
            for prefix, mod in Tests.iteritems():
                if rower['Test'].startswith(prefix):
                    mod.append(rower)
                    mod.sort(key=lambda k: k['Year'])
                    mod.sort(key=lambda k: k['Month'])
                    mod.sort(key=lambda k: k['Day'])

        rower_data['MW'] = maxwatt
        rower_data['FM'] = fortymin
        rower_data['OM'] = onemin
        rower_data['TM'] = twentymin
        rower_data['RM'] = repmax


        return render_template('rower.html', data = rower_data, rower = name)

    else: # request.method == 'GET'
        return render_template('search.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/results/MaxWatt')
def MaxWatts():
    MaxWatt_data = s.searchTest('Max Watt')
    return render_template('MaxWatt.html', data = MaxWatt_data)

@app.route('/results/FortyMinute')
def FortyMinute():
    FortyMin_data = s.searchTest('Forty Minute')
    return render_template('FortyMinute.html', data = FortyMin_data)

@app.route('/results/TwentyMinute')
def TwentyMinute():
    TwentyMin_data = s.searchTest('Twenty Minute')
    return render_template('TwentyMinute.html', data = TwentyMin_data)

@app.route('/results/OneMinute')
def OneMinute():
    OneMin_data = s.searchTest('One Minute')
    return render_template('OneMinute.html', data = OneMin_data)

@app.route('/results/RepMax')
def RepMax():
    RepMax_data = s.searchTest('Rep Max')
    return render_template('RepMax.html', data = RepMax_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0")