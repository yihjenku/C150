import csv
import pymongo
import datetime
import os
from config import MONGO_PORT

def translate(infile):
	keys = []
	MaxWattData = []
	test_date = {}
	test_name = 'Max Watt'
	total_rowers = 0
	with open(infile, 'rU') as f:
		reader = csv.reader(f)
		i = 0
		for row in reader:
			if i == 0:
				date = row[0]
				date = date.replace('/', ' ')
				date = date.split()
				for j in range(3):
					date[j] = int(date[j])
				test_date = {'Day': date[1], 'Month': date[0], 'Year': date[2]}
			elif i == 1:
				keys = row
				# print keys
			else:
				temp = {}
				Day = test_date['Day']
				Month = test_date['Month']
				Year = test_date['Year']
				temp['Day'] = Day
				temp['Month'] = Month
				temp['Year'] = Year
				temp['Date'] = str(Month) + '/' + str(Day) + '/' + str(Year)

				# Rank
				if(row[0] is ''):
					temp[keys[0]] = ''
				else:
					temp[keys[0]] = int(row[0])
					total_rowers = int(row[0])

				# Name
				temp[keys[1]] = row[1].lower()

				# Trial 1
				if(row[2] is ''):
					Trial1 = ''
				else:
					Trial1 = int(row[2])
				temp[keys[2]] = Trial1
				# Trial 2
				if(row[3] is ''):
					Trial2 = ''
				else:
					Trial2 = int(row[3])
				temp[keys[3]] = Trial2
				# Trial 3
				if(row[4] is ''):
					Trial3 = ''
				else:
					Trial3 = int(row[4])
				temp[keys[4]] = Trial3

				if (Trial1 is '' or Trial2 is '' or Trial3 is ''):
					Max = ''
					Avg = ''
				else:
					Max = max(Trial1, Trial2, Trial3)
					Avg = (Trial1 + Trial2 + Trial3) / 3
				temp[keys[5]] = Max
				temp[keys[6]] = Avg

				temp['Test'] = test_name

				MaxWattData.append(temp)
			i += 1
	writeMaxWatt(MaxWattData, total_rowers)

def writeMaxWatt(MaxWattData, total_rowers, outfile = 'Max Watt.txt', database = 'Max Watt'):

	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	# db.drop_collection('Max Watt')
	MaxWatt = db[database]

	# Write to text file
	if not os.path.isdir('outputs'):
 		os.mkdir('outputs')

	file_out = open('outputs/' + outfile, 'w')

	file_out.write('Date' + '\t' + '\t' + 'Rank' + '\t' + 'Name' + '\t' + '\t' + \
					'1' + '\t' + '2' + '\t' + '3' + '\t' + 'Avg' + '\t' + 'High' + '\n')
	file_out.write('\n')

	for i in range(0, len(MaxWattData)):

		if MaxWattData[i]:
			query = {'Day': MaxWattData[i]['Day'], \
					'Month': MaxWattData[i]['Month'], \
					'Year': MaxWattData[i]['Year'], \
					'Name': MaxWattData[i]['Name'].lower(), \
					'Test': 'Max Watt'}
			update = MaxWattData[i]
			update['Rower Total'] = total_rowers
			MaxWatt.update(query, update, True)

	for rower in MaxWatt.find().sort(  [('Year', pymongo.ASCENDING), \
										('Month', pymongo.ASCENDING), \
										('Day', pymongo.ASCENDING), \
										('Rank', pymongo.ASCENDING)] ):
		# print rower
		Month = str(rower['Month'])
		Day = str(rower['Day'])
		Year = str(rower['Year'])
		Rank = str(rower['Rank'])
		Name = rower['Name']
		Trial1 = str(rower['Watt 1'])
		Trial2 = str(rower['Watt 2'])
		Trial3 = str(rower['Watt 3'])
		Avg = str(rower['Average'])
		Max = str(rower['High'])

		if(len(Name)<8):
			if((len(Month) + len(Day) + len(Year)) < 6):
				line = Month + '/' + Day + '/' + Year + '\t' + '\t' + \
						Rank + '\t' + Name + '\t' + '\t' + Trial1 + '\t' + \
						Trial2 + '\t' + Trial3 + '\t' + Avg + '\t' + Max + '\n'
			else:
				line = Month + '/' + Day + '/' + Year + '\t' + Rank + '\t' + \
						Name + '\t' + '\t' + Trial1 + '\t' + Trial2 + '\t' + \
						Trial3 + '\t' + Avg + '\t' + Max + '\n'
		else:
			if((len(Month) + len(Day) + len(Year)) < 6):
				line = Month + '/' + Day + '/' + Year + '\t' + '\t' + \
						Rank + '\t' + Name + '\t' + Trial1 + '\t' + \
						Trial2 + '\t' + Trial3 + '\t' + Avg + '\t' + Max + '\n'
			else:
				line = Month + '/' + Day + '/' + Year + '\t' + \
						Rank + '\t' + Name + '\t' + Trial1 + '\t' + \
						Trial2 + '\t' + Trial3 + '\t' + Avg + '\t' + Max + '\n'
		file_out.write(line)

	file_out.close()
	client.close()

