import csv
import pymongo
import datetime
import os
from config import MONGO_PORT

def translate(infile):
	keys = []
	ThreeByThreeByNinetySecData = []
	test_date = {}
	test_name = '3 by 3 by 90 Second'

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
				temp[keys[1]] = row[1].lower()

				Splits = []
				for k in range(2,12):
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
				ThreeByThreeByNinetySecData.append(temp)
			i += 1

	writeTwoByTwentyMin(ThreeByThreeByNinetySecData, total_rowers)

def writeTwoByTwentyMin(ThreeByThreeByNinetySecData, total_rowers):

	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	# db.drop_collection('2 by 20 Minute')
	TwoByTwentyMinute = db['3 by 3 by 90 Second']

	for i in range(0, len(ThreeByThreeByNinetySecData)):

		if ThreeByThreeByNinetySecData[i]:
			query = {'Day': ThreeByThreeByNinetySecData[i]['Day'], \
					'Month': ThreeByThreeByNinetySecData[i]['Month'], \
					'Year': ThreeByThreeByNinetySecData[i]['Year'], \
					'Name': ThreeByThreeByNinetySecData[i]['Name'].lower(), \
					'Test': '3 by 3 by 90 Second'}
			update = ThreeByThreeByNinetySecData[i]
			update['Rower Total'] = total_rowers
			TwoByTwentyMinute.update(query, update, True)
			print ThreeByThreeByNinetySecData[i]

	client.close()

