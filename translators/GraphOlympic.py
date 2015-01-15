import pygal
import pymongo
import search as s

def graphOlympic(name):

	client = pymongo.MongoClient('localhost', 27017)
	db = client['C150']
	s.search(name)
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

	radar_chart = pygal.Radar()
	radar_chart.title = Name
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

	radar_chart.render_to_file('static/OlympicGraphs/' + Name + '.svg')

