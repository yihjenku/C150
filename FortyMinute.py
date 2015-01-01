import csv
import pymongo
import datetime

def readFortyMinute(infile):
	keys = []
	FortyMinData = []
	test_date = {}
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
				temp['Day'] = test_date['Day']
				temp['Month'] = test_date['Month']
				temp['Year'] = test_date['Year']
				if(row[0] is ''):
					Rank = ''
				else:
					Rank = int(row[0])
				temp[keys[0]] = Rank

				Name = row[1]
				temp[keys[1]] = Name

				for k in range(2,13):
					if(row[k] is ''):
						Test_Split = {'Minute': '', 'Second': '', 'Millisecond': ''}
					else:
						Split = row[k]
						Split = Split.replace(':', ' ')
						Split = Split.replace('.', ' ')
						Split = Split.split()
						for j in range(3):
							Split[j] = int(Split[j])
						Test_Split = {'Minute': Split[0], 'Second': Split[1], 
										'Millisecond': Split[2]}
					temp[keys[k]] = Test_Split
				
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

				temp['Test'] = 'Forty Minute'
				FortyMinData.append(temp)
			i += 1
	writeFortyMinute(FortyMinData)

def writeFortyMinute(FortyMinData):

	client = pymongo.MongoClient('localhost', 27017)
	db = client['C150']
	# db.drop_collection('Forty Minute')
	FortyMinute = db['Forty Minute']

	# Write to text file
	textfilename = 'Forty Minute.txt'
	file_out = open(textfilename, 'w')

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
					'Name': FortyMinData[i]['Name'], \
					'Test': 'Forty Minute'}
			update = FortyMinData[i]
			FortyMinute.update(query, update, True)

	# FortyMinute.find().sort('Rank',pymongo.DESCENDING)

	for rower in FortyMinute.find(): #.sort([('Month',pymongo.ASCENDING),('Rank',pymongo.ASCENDING)]):
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

