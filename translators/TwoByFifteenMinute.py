import csv
import pymongo
import datetime
import os
from config import MONGO_PORT

def translate(infile):
	keys = []
	TwoByFifteenMinData = []
	test_date = {}
	test_name = '2 by 15 Minute'

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
				for k in range(2,6):
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
				for k in range(7,11):
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

				if(row[6] is ''):
					Distance1 = ''
				else:
					Distance1 = int(row[6])
				temp[keys[6]] = Distance1
				if(row[11] is ''):
					Distance2 = ''
				else:
					Distance2 = int(row[11])
				temp[keys[11]] = Distance2
				if(row[12] is ''):
					TotalDistance = ''
				else:
					TotalDistance = int(row[12])
				temp[keys[12]] = TotalDistance


				temp['Test'] = test_name
				TwoByFifteenMinData.append(temp)
			i += 1

	writeTwoByFifteenMin(TwoByFifteenMinData, total_rowers)

def writeTwoByFifteenMin(TwoByFifteenMinData, total_rowers):

	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	# db.drop_collection('2 by 15 Minute')
	TwoByFifteenMinute = db['2 by 15 Minute']

	for i in range(0, len(TwoByFifteenMinData)):

		if TwoByFifteenMinData[i]:
			query = {'Day': TwoByFifteenMinData[i]['Day'], \
					'Month': TwoByFifteenMinData[i]['Month'], \
					'Year': TwoByFifteenMinData[i]['Year'], \
					'Name': TwoByFifteenMinData[i]['Name'], \
					'Test': '2 by 15 Minute'}
			update = TwoByFifteenMinData[i]
			update['Rower Total'] = total_rowers
			TwoByFifteenMinute.update(query, update, True)
			print TwoByFifteenMinData[i]

	client.close()