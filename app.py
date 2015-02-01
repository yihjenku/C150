from flask import Flask, render_template, request
import requests
from translators import search as s, Graphics as g
import import_data
from AddInfo import add_info

app = Flask(__name__)
app.config['DEBUG'] = True  # Disable this for deployment

@app.route('/', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':

        import_data.import_data()

        maxwatt = []
        fortymin = []
        onemin = []
        twentymin = []
        repmax = []
        fourbyfivemin = []
        fivebyfivemin = []
        twobyfifteenmin = []
        twobytwentymin = []
        threebythreebyninetysec = []
        threebythreebytwomin = []

        Tests = {'Max Watt': maxwatt, 'Twenty Minute': twentymin, 'One Minute': onemin, \
            'Forty Minute': fortymin, 'Rep Max': repmax, '4 by 5 Minute': fourbyfivemin, \
            '5 by 5 Minute': fivebyfivemin, '2 by 15 Minute': twobyfifteenmin, \
            '2 by 20 Minute': twobytwentymin, '3 by 3 by 90 Second': threebythreebyninetysec, \
            '3 by 3 by 2 Minute': threebythreebytwomin}

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

        for member in add_info['items']:
            if name == member['Last']:
                rower_data['First'] = member['First']
                rower_data['Last'] = member['Last']
                rower_data['School'] = member['School']
                rower_data['Year'] = member['Year']
                rower_data['Side'] = member['Side']

        rower_data['MW'] = maxwatt
        rower_data['FM'] = fortymin
        rower_data['OM'] = onemin
        rower_data['TM'] = twentymin
        rower_data['RM'] = repmax
        rower_data['4x5Min'] = fourbyfivemin
        rower_data['5x5Min'] = fivebyfivemin
        rower_data['2x15Min'] = twobyfifteenmin
        rower_data['2x20Min'] = twobytwentymin
        rower_data['3x3x90Sec'] = threebythreebyninetysec
        rower_data['3x3x2Min'] = threebythreebytwomin

        return render_template('rower.html', data = rower_data, rower = name)

    else: # request.method == 'GET'
        return render_template('search.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/results/MaxWatt')
def MaxWatts():
    rower_items = {}
    rower_items['items'] = s.searchTest('Max Watt')
    return render_template('MaxWatt.html', data = rower_items)

@app.route('/results/FortyMinute')
def FortyMinute():
    rower_items = {}
    rower_items['items'] = s.searchTest('Forty Minute')
    return render_template('FortyMinute.html', data = rower_items)

@app.route('/results/TwentyMinute')
def TwentyMinute():
    rower_items = {}
    rower_items['items'] = s.searchTest('Twenty Minute')
    return render_template('TwentyMinute.html', data = rower_items)

@app.route('/results/OneMinute')
def OneMinute():
    rower_items = {}
    rower_items['items'] = s.searchTest('One Minute')
    return render_template('OneMinute.html', data = rower_items)

@app.route('/results/RepMax')
def RepMax():
    rower_items = {}
    rower_items['items'] = s.searchTest('Rep Max')
    return render_template('RepMax.html', data = rower_items)

@app.route('/results/Redline')
def Redline():
    rower_items = {}
    rower_items['2x15Min'] = s.searchTest('2 by 15 Minute')
    rower_items['2x20Min'] = s.searchTest('2 by 20 Minute')
    return render_template('Redline.html', data = rower_items)

@app.route('/results/AT1')
def ATOne():
    rower_items = {}
    rower_items['4x5Min'] = s.searchTest('4 by 5 Minute')
    rower_items['5x5Min'] = s.searchTest('5 by 5 Minute')
    rower_items['3x3x2Min'] = s.searchTest('3 by 3 by 2 Minute')
    rower_items['3x3x90Sec'] = s.searchTest('3 by 3 by 90 Second')
    return render_template('AT1.html', data = rower_items)

if __name__ == '__main__':
    app.run(host="0.0.0.0")