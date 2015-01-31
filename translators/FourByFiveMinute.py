import csv
import pymongo
import datetime
import os
from config import MONGO_PORT

def translate(infile):
	keys = []
	FourByFiveMinData = []
	test_date = {}
	test_name = '4 by 5 Minute'

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

				if(row[0] is ''):
					Rank = ''
				else:
					Rank = int(row[0])
					total_rowers = int(row[0])
				temp[keys[0]] = Rank

				 # Name
				temp[keys[1]] = row[1]

				Splits = []
				for k in range(2,7):
					if(row[k] is ''):
						Test_Split = {'Minute': '', 'Second': '', 'Millisecond': ''}
						Splits.append(Test_Split)
					else:
						Split = row[k]
						Split_String = Split
						Split = Split.replace(':', ' ')
						Split = Split.replace('.', ' ')
						Split = Split.split()
						for j in range(3):
							Split[j] = int(Split[j])
						Test_Split = {'Minute': Split[0], 'Second': Split[1],
										'Millisecond': Split[2], 'String': Split_String}
						Splits.append(Test_Split)
					temp[keys[k]] = Test_Split

				temp['Test'] = test_name
				FourByFiveMinData.append(temp)
			i += 1

	writeFourByFiveMin(FourByFiveMinData, total_rowers)

def writeFourByFiveMin(FourByFiveMinData, total_rowers):

	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	# db.drop_collection('Forty Minute')
	FourByFiveMinute = db['4 by 5 Minute']

	for i in range(0, len(FourByFiveMinData)):

		if FourByFiveMinData[i]:
			query = {'Day': FourByFiveMinData[i]['Day'], \
					'Month': FourByFiveMinData[i]['Month'], \
					'Year': FourByFiveMinData[i]['Year'], \
					'Name': FourByFiveMinData[i]['Name'], \
					'Test': '4 by 5 Minute'}
			update = FourByFiveMinData[i]
			update['Rower Total'] = total_rowers
			FourByFiveMinute.update(query, update, True)

	client.close()

