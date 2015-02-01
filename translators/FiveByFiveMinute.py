import csv
import pymongo
import datetime
import os
from config import MONGO_PORT

def translate(infile):
	keys = []
	FiveByFiveMinData = []
	test_date = {}
	test_name = '5 by 5 Minute'

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
				for k in range(2,8):
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

				if(row[8] is ''):
					Weight = ''
				else:
					Weight = float(row[8])
				temp[keys[8]] = Weight

				temp['Test'] = test_name
				FiveByFiveMinData.append(temp)
			i += 1

	writeFourByFiveMin(FiveByFiveMinData, total_rowers)

def writeFourByFiveMin(FiveByFiveMinData, total_rowers):

	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	db.drop_collection('5 by 5 Minute')
	FourByFiveMinute = db['5 by 5 Minute']

	for i in range(0, len(FiveByFiveMinData)):

		if FiveByFiveMinData[i]:
			query = {'Day': FiveByFiveMinData[i]['Day'], \
					'Month': FiveByFiveMinData[i]['Month'], \
					'Year': FiveByFiveMinData[i]['Year'], \
					'Name': FiveByFiveMinData[i]['Name'], \
					'Test': '5 by 5 Minute'}
			update = FiveByFiveMinData[i]
			update['Rower Total'] = total_rowers
			FourByFiveMinute.update(query, update, True)

	client.close()
