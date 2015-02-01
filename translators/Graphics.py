import pygal
from pygal.style import BlueStyle, LightenStyle
import pymongo
import search as s
import os
from config import MONGO_PORT

def graphOlympic(name):

	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	s.searchRower(name)
	RowerDB = db[name]

	WeightData = []

	FortyMinuteData = []
	for rower in RowerDB.find({'Test': 'Forty Minute'}) \
						.sort( [('Year', pymongo.ASCENDING), \
								('Month', pymongo.ASCENDING), \
								('Rank', pymongo.ASCENDING)] ):

		if (isinstance(rower['Meters'], basestring)):
			FortyMinuteData.append(0)
		else:
			FortyMinuteData.append(rower['Meters'])

		if not (isinstance(rower['Weight'], basestring)):
			WeightData.append(rower['Weight'])
	# print FortyMinuteData

	OneMinuteData = []
	for rower in RowerDB.find({'Test': 'One Minute'}) \
						.sort([('Year', pymongo.ASCENDING), \
								('Month', pymongo.ASCENDING), \
								('Rank', pymongo.ASCENDING)]):

		if (isinstance(rower['Meters'], basestring)):
			OneMinuteData.append(0)
		else:
			OneMinuteData.append(rower['Meters'])

		if not (isinstance(rower['Weight'], basestring)):
			WeightData.append(rower['Weight'])
	# print OneMinuteData

	RepMaxData = []
	for rower in RowerDB.find({'Test': 'Rep Max'}) \
						.sort([('Year', pymongo.ASCENDING), \
								('Month', pymongo.ASCENDING), \
								('Rank', pymongo.ASCENDING)]):
		if (isinstance(rower['Average'], basestring)):
			RepMaxData.append(0)
		else:
			RepMaxData.append(rower['Average'])
	# print RepMaxData

	MaxWattData = []
	for rower in RowerDB.find({'Test': 'Max Watt'}) \
						.sort([('Year', pymongo.ASCENDING), \
								('Month', pymongo.ASCENDING), \
								('Rank', pymongo.ASCENDING)]):
		if (isinstance(rower['High'], basestring)):
			MaxWattData.append(0)
		else:
			MaxWattData.append(rower['High'])
	# print MaxWattData

	# print WeightData
	weight = weightCalc(WeightData)

	plotRadar(name, weight, FortyMinuteData, OneMinuteData, RepMaxData, MaxWattData)


def RMAverage(squat, deadlift):
	return (squat + deadlift)/2


def percentCalc(athleteValue, olympicValue):
	return round((athleteValue/float(olympicValue)), 4)


def weightCalc(weightdata):
	sum = 0
	for entry in weightdata:
		sum += entry
	if not (sum == 0):
		weight = round(float(sum/len(weightdata)), 2)
	# print ('%.1f' % weight)
	return weight


def plotRadar(Name, Weight, FMData, OMData, RMData, MWData):
	# Olympic level constants
	OlympicFortyTD = 11881 # Meters rowed in 40 minutes
	OlympicOneTD = 375 # Meters rowed in 1 minute
	OlympicMaxWatt = 1100 # Maximum watts generated
	Weight *= 2

	dark_lighten_style = LightenStyle('#66CCFF', step = 5)
	radar_chart = pygal.Radar(fill = False, style = dark_lighten_style)
	radar_chart.title = Name + ' Olympic Comparison'
	radar_chart.x_labels = ['40 Minute', '1 Minute', '1 Rep Max', 'Max Watt']

	for i in range(len(FMData)):
		Title = 'Battery ' + str(i+1)
		percentForty = percentCalc(FMData[i], OlympicFortyTD)
		percentOne = percentCalc(OMData[i], OlympicOneTD)
		percentRM = percentCalc(RMData[i], Weight)
		percentMaxWatt = percentCalc(MWData[i], OlympicMaxWatt)
		# print [percentForty, percentOne, percentRM, percentMaxWatt]
		radar_chart.add(Title, [percentForty, percentOne, percentRM, percentMaxWatt])

	radar_chart.add('Olympic Standard', [1, 1, 1, 1,])

	if not os.path.isdir('static/OlympicGraphs/'):
 		os.mkdir('static/OlympicGraphs/')

	radar_chart.render_to_file('static/OlympicGraphs/' + Name + '.svg')

def graphSplitChanges(name):
	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	s.searchRower(name)
	RowerDB = db[name]

	for rower in RowerDB.find({'Test': 'Forty Minute'}) \
						.sort( [('Year', pymongo.ASCENDING), \
								('Month', pymongo.ASCENDING), \
								('Rank', pymongo.ASCENDING)] ):
		FortyMinRowerData = []
		FortyMinTeamData = []
		for m in range(2,11):
			key = str(m*4)
			if rower['FortySplitChanges'][key]['String'] == '':
				FortyMinRowerData.append(0)
			else:
				FortyMinRowerData.append(float(rower['FortySplitChanges'][key]['String']))
			FortyMinTeamData.append(rower['40AvgSplitChange'][key])
		plotLinear(name, FortyMinRowerData, FortyMinTeamData, 'Forty Minute', rower['index'])

	for rower in RowerDB.find({'Test': 'Twenty Minute'}) \
						.sort( [('Year', pymongo.ASCENDING), \
								('Month', pymongo.ASCENDING), \
								('Rank', pymongo.ASCENDING)] ):
		TwentyMinRowerData = []
		TwentyMinTeamData = []
		for m in range(2,11):
			key = str(m*2)
			if rower['TwentySplitChanges'][key]['String'] == '':
				TwentyMinRowerData.append(0)
			else:
				TwentyMinRowerData.append(float(rower['TwentySplitChanges'][key]['String']))
			TwentyMinTeamData.append(rower['20AvgSplitChange'][key])
		plotLinear(name, TwentyMinRowerData, TwentyMinTeamData, 'Twenty Minute', rower['index'])


def plotLinear(Name, RowerData, TeamData, TestType, TestNumber):
	dark_lighten_style = LightenStyle('#66CCFF', step = 5)
	line_chart = pygal.Line(fill = True, interpolate='cubic', style = dark_lighten_style)
	line_chart.title = Name + ' vs. Team ' + 'Split Comparison for ' + TestType + ' ' + str(TestNumber)
	line_chart.x_labels = map(str, range(1, 10))
	line_chart.add(Name, RowerData)
	line_chart.add('Team Average', TeamData)
	if TestType == 'Forty Minute':
		if not os.path.isdir('static/FortyMinute/'):
 			os.mkdir('static/FortyMinute/')
		line_chart.render_to_file('static/FortyMinute/' + Name + str(TestNumber) + '.svg')
	if TestType == 'Twenty Minute':
		if not os.path.isdir('static/TwentyMinute/'):
			os.mkdir('static/TwentyMinute/')
		line_chart.render_to_file('static/TwentyMinute/' + Name + str(TestNumber) + '.svg')