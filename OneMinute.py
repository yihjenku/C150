import csv
import pymongo
import datetime

def readOneMinute(infile):
	keys = []
	OneMinData = []
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
				print keys
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

				if(row[2] is ''):
					Test_AvgSplit = {'Minute': '', 'Second': '', 'Millisecond': ''}
				else:
					AvgSplit = row[2]
					AvgSplit = AvgSplit.replace(':', ' ')
					AvgSplit = AvgSplit.replace('.', ' ')
					AvgSplit = AvgSplit.split()
					for j in range(3):
						AvgSplit[j] = int(AvgSplit[j])
					Test_AvgSplit = {'Minute': AvgSplit[0], 'Second': AvgSplit[1], 
									'Millisecond': AvgSplit[2]}
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

				temp['Test'] = 'One Minute'

				OneMinData.append(temp)
			i += 1
	writeOneMinute(OneMinData)

def writeOneMinute(OneMinData):

	client = pymongo.MongoClient('localhost', 27017)
	db = client['C150']
	# db.drop_collection('One Minute')
	OneMinute = db['One Minute']

	# Write to text file
	textfilename = 'One Minute.txt'
	file_out = open(textfilename, 'w')
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
			OneMinute.update(query, update, True)

	for rower in OneMinute.find():
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

