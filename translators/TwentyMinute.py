import csv
import pymongo
import datetime
import os
from config import MONGO_PORT

def translate(infile):
	keys = []
	TwentyMinData = []
	test_date = {}
	test_name = 'Twenty Minute'
	total_rowers = 0
	split_change_ave = {}
	split_change_count = {}
	for n in range (2,11):
		split_change_ave[str(n*2)] = 0.0
		split_change_count[str(n*2)] = 0

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
				for k in range(2,13):
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
				Split_Changes = get_Split_Changes(Splits)

				temp['TwentySplitChanges'] = Split_Changes

				for m in range(2,11):
					key = str(m*2)
					if Split_Changes[key]['String'] is not '':
						split_change_count[key] += 1
						a = float(Split_Changes[key]['String'])
						b = split_change_count[key]-1
						c = split_change_ave[key]
						d = split_change_count[key]
						split_change_ave[key] = (c*b + a)/d

				if(row[13] is ''):
					AvgSPM = ''
				else:
					AvgSPM = int(row[13])
				temp[keys[13]] = AvgSPM

				if(row[14] is ''):
					Meters = ''
				else:
					Meters = int(row[14])
				temp[keys[14]] = Meters

				if(row[15] is ''):
					Weight = ''
				else:
					Weight = float(row[15])
				temp[keys[15]] = Weight

				temp['Test'] = test_name
				TwentyMinData.append(temp)

			i += 1

	for n in range (2,11):
		split_change_ave[str(n*2)] = round(split_change_ave[str(n*2)], 2)

	writeTwentyMinute(TwentyMinData, total_rowers, split_change_ave)

def writeTwentyMinute(TwentyMinData, total_rowers, split_change_ave):

	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	# db.drop_collection('Twenty Minute')
	TwentyMinute = db['Twenty Minute']

	# Write to text file
	textfilename = 'Twenty Minute.txt'

	if not os.path.isdir('outputs'):
 		os.mkdir('outputs')

	file_out = open('outputs/' + textfilename, 'w')

	file_out.write('Date' + '\t' + '\t' + 'Rank' + '\t' + 'Name' + '\t' + '\t' + \
					'2' + '\t' + '4' + '\t' + '6' + '\t' + '8' + '\t' + '10' + '\t' +
					'12' + '\t' + '14' + '\t' + '16' + '\t' + '18' + '\t' + '20' + '\t' +
					'Avg Split' + '\t' + 'AvgSPM' + '\t' + 'Meters' + '\t' + 'Weight' + '\n')
	file_out.write('\n')

	for i in range(0, len(TwentyMinData)):

		if TwentyMinData[i]:
			query = {'Day': TwentyMinData[i]['Day'], \
					'Month': TwentyMinData[i]['Month'], \
					'Year': TwentyMinData[i]['Year'], \
					'Name': TwentyMinData[i]['Name'], \
					'Test': 'Twenty Minute'}
			update = TwentyMinData[i]
			update['Rower Total'] = total_rowers
			update['20AvgSplitChange'] = split_change_ave
			TwentyMinute.update(query, update, True)

	for rower in TwentyMinute.find().sort( [('Year', pymongo.ASCENDING), \
											('Month', pymongo.ASCENDING), \
											('Day', pymongo.ASCENDING), \
											('Rank', pymongo.ASCENDING)] ):
		# print rower
		Month = str(rower['Month'])
		Day = str(rower['Day'])
		Year = str(rower['Year'])
		Date = Month + '/' + Day + '/' + Year

		Rank = str(rower['Rank'])
		Name = rower['Name']

		Splits = []
		Splits_String = ''
		for j in range(10):
			temp_str = str((j+1)*2)
			Minute = str(rower[temp_str]['Minute'])
			if(rower[temp_str]['Second'] < 10):
				Second = '0' + str(rower[temp_str]['Second'])
			else:
				Second = str(rower[temp_str]['Second'])
			MilSec = str(rower[temp_str]['Millisecond'])
			if (Minute is '' or Second is '' or MilSec is ''):
				Splits.append('')
			else:
				Splits.append(Minute + ':' + Second + '.' + MilSec)
			Splits_String = Splits_String + Splits[j] + '\t'

		Minute = str(rower['Avg Split']['Minute'])
		if(rower['Avg Split']['Second'] < 10):
			Second = '0' + str(rower['Avg Split']['Second'])
		else:
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
				line = Date + '\t' + '\t' + \
						Rank + '\t' + Name + '\t' + '\t' + \
						Splits_String + AvgSplit + '\t' + '\t' + \
						Meters + '\t' + AvgSPM + '\t' + Weight + '\n'
			else:
				line = Date + '\t' + \
						Rank + '\t' + Name + '\t' + '\t' + \
						Splits_String + AvgSplit + '\t' + '\t' + \
						Meters + '\t' + AvgSPM + '\t' + Weight + '\n'
		else:
			if((len(Month) + len(Day) + len(Year)) < 6):
				line = Date + '\t' + '\t' + \
						Rank + '\t' + Name + '\t' + \
						Splits_String + AvgSplit + '\t' + '\t' + \
						Meters + '\t' + AvgSPM + '\t' + Weight + '\n'
			else:
				line = Date + '\t' + \
						Rank + '\t' + Name + '\t' + \
						Splits_String + AvgSplit + '\t' + '\t' + \
						Meters + '\t' + AvgSPM + '\t' + Weight + '\n'
		file_out.write(line)

	file_out.close()
	client.close()

def get_Split_Changes(Splits, intervals = 2):

	Split_Changes = {}
	for i in range(1, len(Splits)-1):
		temp_changes = {}
		if(Splits[i]['Minute'] is '' or Splits[i]['Second'] is '' or Splits[i]['Millisecond'] is '' or \
			Splits[i-1]['Minute'] is '' or Splits[i-1]['Second'] is '' or Splits[i-1]['Millisecond'] is ''):
			temp_changes['Minute'] = ''
			temp_changes['Second'] = ''
			temp_changes['Millisecond'] = ''
			temp_changes['String'] = ''
		else:
			seconds_1 = float(Splits[i-1]['Minute']*60) + float(Splits[i-1]['Second']) + float(Splits[i-1]['Millisecond'])/10
			seconds_2 = float(Splits[i]['Minute']*60) + float(Splits[i]['Second']) + float(Splits[i]['Millisecond'])/10
			difference = int(round((seconds_2 - seconds_1)*10))
			if difference > 0:
				temp_changes['Millisecond'] = difference%10
				seconds = difference/10
			else:
				temp_changes['Millisecond'] = (-1*difference)%10
				seconds = (-1*difference)/10
			if seconds_2 < seconds_1:
				temp_changes['Second'] = -1*(seconds%60)
				if seconds is 0:
					temp_changes['String'] = '-' + str(temp_changes['Second']) + '.' + str(temp_changes['Millisecond'])
				else:
					temp_changes['String'] = str(temp_changes['Second']) + '.' + str(temp_changes['Millisecond'])
			else:
				temp_changes['Second'] = seconds%60
				temp_changes['String'] = str(temp_changes['Second']) + '.' + str(temp_changes['Millisecond'])
			temp_changes['Minute'] = seconds/60

		Split_Changes[str((i+1)*intervals)] = temp_changes

	return Split_Changes




