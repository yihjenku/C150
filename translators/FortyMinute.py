import csv
import pymongo
import datetime
import os
import TwentyMinute as tm
from config import MONGO_PORT

def translate(infile):
	keys = []
	FortyMinData = []
	test_date = {}
	test_name = 'Forty Minute'
	split_change_ave = {}
	split_change_count = {}
	for n in range (2,11):
		split_change_ave[str(n*4)] = 0.0
		split_change_count[str(n*4)] = 0

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
				Split_Changes = tm.get_Split_Changes(Splits, 4)
				temp['FortySplitChanges'] = Split_Changes

				for m in range(2,11):
					key = str(m*4)
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
				FortyMinData.append(temp)
			i += 1

	for n in range (2,11):
		split_change_ave[str(n*4)] = round(split_change_ave[str(n*4)], 2)
	writeFortyMinute(FortyMinData, total_rowers, split_change_ave)

def writeFortyMinute(FortyMinData, total_rowers, split_change_ave):

	client = pymongo.MongoClient('localhost', MONGO_PORT)
	db = client['C150']
	# db.drop_collection('Forty Minute')
	FortyMinute = db['Forty Minute']

	# Write to text file
	textfilename = 'Forty Minute.txt'

	if not os.path.isdir('outputs'):
 		os.mkdir('outputs')

	file_out = open('outputs/' + textfilename, 'w')

	Keys_String = ''
	for j in range(10):
		temp_str = str((j+1)*4)
		Keys_String = Keys_String + temp_str + '\t'

	file_out.write('Date' + '\t' + '\t' + 'Rank' + '\t' + 'Name' + '\t' + '\t' + \
					Keys_String + \
					'Avg Split' + '\t' + 'AvgSPM' + '\t' + 'Meters' + '\t' + 'Weight' + '\n')
	file_out.write('\n')

	for i in range(0, len(FortyMinData)):

		if FortyMinData[i]:
			query = {'Day': FortyMinData[i]['Day'], \
					'Month': FortyMinData[i]['Month'], \
					'Year': FortyMinData[i]['Year'], \
					'Name': FortyMinData[i]['Name'].lower(), \
					'Test': 'Forty Minute'}
			update = FortyMinData[i]
			update['Rower Total'] = total_rowers
			update['40AvgSplitChange'] = split_change_ave
			FortyMinute.update(query, update, True)

	for rower in FortyMinute.find().sort(  [('Year', pymongo.ASCENDING), \
											('Month', pymongo.ASCENDING), \
											('Day', pymongo.ASCENDING), \
											('Rank', pymongo.ASCENDING)] ):
		# print rower
		Month = str(rower['Month'])
		Day = str(rower['Day'])
		Year = str(rower['Year'])
		Date = Month + '/' + Day + '/' + Year

		Rank = str(rower['Rank'])
		Name = rower['Name'].title()

		Splits = []
		Splits_String = ''
		for j in range(10):
			temp_str = str((j+1)*4)
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

