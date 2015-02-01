import csv
import pymongo
import datetime
import os
from config import MONGO_PORT

def translate(infile):
	keys = []
	OneMinData = []
	test_date = {}
	test_name = 'One Minute'
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

				if(row[0] is ''):
					Rank = ''
				else:
					Rank = int(row[0])
					total_rowers = int(row[0])
				temp[keys[0]] = Rank

				# Name
				temp[keys[1]] = row[1]

				if(row[2] is ''):
					Test_AvgSplit = {'Minute': '', 'Second': '', 'Millisecond': ''}
				else:
					AvgSplit = row[2]
					Split_String = AvgSplit
					AvgSplit = AvgSplit.replace(':', ' ')
					AvgSplit = AvgSplit.replace('.', ' ')
					AvgSplit = AvgSplit.split()
					for j in range(3):
						AvgSplit[j] = int(AvgSplit[j])
					Test_AvgSplit = {'Minute': AvgSplit[0], 'Second': AvgSplit[1],
									'Millisecond': AvgSplit[2], 'String': Split_String}
				temp[keys[2]] = Test_AvgSplit

				if(row[3] is ''):
					Meters = ''
				else:
					Meters = int(row[3])
				temp[keys[3]] = Meters

				if(row[4] is ''):
					AvgSPM = ''
				else:
					AvgSPM = int(row[4])
				temp[keys[4]] = AvgSPM

				if(row[5] is ''):
					Weight = ''
				else:
					Weight = float(row[5])
				temp[keys[5]] = Weight

				temp['Test'] = test_name

				OneMinData.append(temp)
			i += 1
	writeOneMinute(OneMinData, total_rowers)

def writeOneMinute(OneMinData, total_rowers):

	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	#db.drop_collection('One Minute')
	OneMinute = db['One Minute']

	# Write to text file
	textfilename = 'One Minute.txt'

	if not os.path.isdir('outputs'):
 		os.mkdir('outputs')

	file_out = open('outputs/' + textfilename, 'w')

	file_out.write('Date' + '\t' + '\t' + 'Rank' + '\t' + 'Name' + '\t' + '\t' + \
					'Avg Split' + '\t' + 'Meters' + '\t' + 'AvgSPM' + '\t' + 'Weight' + '\n')
	file_out.write('\n')

	for i in range(0, len(OneMinData)):

		if OneMinData[i]:
			query = {'Day': OneMinData[i]['Day'], \
					'Month': OneMinData[i]['Month'], \
					'Year': OneMinData[i]['Year'], \
					'Name': OneMinData[i]['Name'], \
					'Test': 'One Minute'}
			update = OneMinData[i]
			update['Rower Total'] = total_rowers
			OneMinute.update(query, update, True)

	for rower in OneMinute.find().sort([('Year', pymongo.ASCENDING), \
										('Month', pymongo.ASCENDING), \
										('Day', pymongo.ASCENDING), \
										('Rank', pymongo.ASCENDING)] ):
		# print rower
		Month = str(rower['Month'])
		Day = str(rower['Day'])
		Year = str(rower['Year'])
		Rank = str(rower['Rank'])
		Name = rower['Name']
		Minute = str(rower['Avg Split']['Minute'])
		Second = str(rower['Avg Split']['Second'])
		MilSec = str(rower['Avg Split']['Millisecond'])
		if (Minute is '' or Second is '' or MilSec is ''):
			AvgSplit = ''
		else:
			AvgSplit = Minute + ':' + Second + '.' + MilSec
		Meters = str(rower['Meters'])
		AvgSPM = str(rower['Avg SPM'])
		Weight = str(rower['Weight'])

		if(len(Name)<8):
			if((len(Month) + len(Day) + len(Year)) < 6):
				line = Month + '/' + Day + '/' + Year + '\t' + '\t' + \
						Rank + '\t' + Name + '\t' + '\t' + \
						AvgSplit + '\t' + '\t' + \
						Meters + '\t' + AvgSPM + '\t' + Weight + '\n'
			else:
				line = Month + '/' + Day + '/' + Year + '\t' + \
						Rank + '\t' + Name + '\t' + '\t' + \
						AvgSplit + '\t' + '\t' + \
						Meters + '\t' + AvgSPM + '\t' + Weight + '\n'
		else:
			if((len(Month) + len(Day) + len(Year)) < 6):
				line = Month + '/' + Day + '/' + Year + '\t' + '\t' + \
						Rank + '\t' + Name + '\t' + \
						AvgSplit + '\t' + '\t' + \
						Meters + '\t' + AvgSPM + '\t' + Weight + '\n'
			else:
				line = Month + '/' + Day + '/' + Year + '\t' + \
						Rank + '\t' + Name + '\t' + \
						AvgSplit + '\t' + '\t' + \
						Meters + '\t' + AvgSPM + '\t' + Weight + '\n'
		file_out.write(line)

	file_out.close()
	client.close()