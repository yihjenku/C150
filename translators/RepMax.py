import csv
import pymongo
import datetime
import os
from config import MONGO_PORT

def translate(infile):
	keys = []
	RepMaxData = []
	test_date = {}
	test_name = 'Rep Max'
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
				temp[keys[1]] = row[1]

				# Squat
				if(row[2] is ''):
					Squat = ''
				else:
					Squat = row[2]
				temp[keys[2]] = Squat

				# Deadlift
				if(row[3] is ''):
					Deadlift = ''
				else:
					Deadlift = int(row[3])
				temp[keys[3]] = Deadlift

				# Average
				if(Squat is '' and Deadlift is ''):
					Average = ''
				elif(Squat is ''):
					Average = float(Deadlift)
				elif(Deadlift is ''):
					Average = float(Squat)
				else:
					Average = float((int(Deadlift) + int(Squat)))/2
				temp[keys[4]] = Average

				temp['Test'] = test_name

				RepMaxData.append(temp)
			i += 1
	writeRepMax(RepMaxData, total_rowers)

def writeRepMax(RepMaxData, total_rowers):

	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	# db.drop_collection('Rep Max')
	RepMax = db['Rep Max']

	# Write to text file
	textfilename = 'Rep Max.txt'

	if not os.path.isdir('outputs'):
 		os.mkdir('outputs')

	file_out = open('outputs/' + textfilename, 'w')

	file_out.write('Date' + '\t' + '\t' + 'Rank' + '\t' + 'Name' + '\t' + '\t' + \
					'Squat' + '\t' + '\t' + 'Deadlift' + '\t' + 'Average' + '\n')
	file_out.write('\n')

	for i in range(0, len(RepMaxData)):

		if RepMaxData[i]:
			query = {'Day': RepMaxData[i]['Day'], \
					'Month': RepMaxData[i]['Month'], \
					'Year': RepMaxData[i]['Year'], \
					'Name': RepMaxData[i]['Name'], \
					'Test': 'Rep Max'}
			update = RepMaxData[i]
			update['Rower Total'] = total_rowers
			RepMax.update(query, update, True)

	for rower in RepMax.find().sort([('Year', pymongo.ASCENDING), \
									('Month', pymongo.ASCENDING), \
									('Day', pymongo.ASCENDING), \
									('Rank', pymongo.ASCENDING)] ):
		# print rower
		Month = str(rower['Month'])
		Day = str(rower['Day'])
		Year = str(rower['Year'])
		Rank = str(rower['Rank'])
		Name = rower['Name']
		Squat = str(rower['Squat'])
		Deadlift = str(rower['Deadlift'])
		Average = str(rower['Average'])

		if(len(Name)<8):
			if((len(Month) + len(Day) + len(Year)) < 6):
				line = Month + '/' + Day + '/' + Year + '\t' + '\t' + \
						Rank + '\t' + Name + '\t' + '\t' + \
						Squat + '\t' + '\t' + Deadlift + '\t' + '\t' + \
						Average + '\n'
			else:
				line = Month + '/' + Day + '/' + Year + '\t' + \
						Rank + '\t' + Name + '\t' + '\t' + \
						Squat + '\t' + '\t' + Deadlift + '\t' + '\t' + \
						Average + '\n'
		else:
			if((len(Month) + len(Day) + len(Year)) < 6):
				line = Month + '/' + Day + '/' + Year + '\t' + '\t' + \
						Rank + '\t' + Name + '\t' + \
						Squat + '\t' + '\t' + Deadlift + '\t' + '\t' + \
						Average + '\n'
			else:
				line = Month + '/' + Day + '/' + Year + '\t' + \
						Rank + '\t' + Name + '\t' + \
						Squat + '\t' + '\t' + Deadlift + '\t' + '\t' + \
						Average + '\n'
		file_out.write(line)

	file_out.close()
	client.close()