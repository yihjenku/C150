import pymongo
import MaxWatt as mw

def search(name):
	
	client = pymongo.MongoClient('localhost', 27017)
	db = client['C150']
	db.drop_collection(name)
	RowerDB = db[name]
	RowerData = []
	Tests = ['Max Watt', 'Twenty Minute', 'One Minute', 'Forty Minute', 'Rep Max']

	for test in Tests:
		database = db[test]
		for rower in database.find({'Name': name}):
			# print rower
			RowerData.append(rower)
			query = {'Day': rower['Day'], \
					'Month': rower['Month'], \
					'Year': rower['Year'], \
					'Name': rower['Name'], \
					'Test': rower['Test']}
			update = rower
			RowerDB.update(query, update, True)
	

	# for entry in RowerDB.find():
		# print entry

	client.close()


	# TwentyMinute = db['Twenty Minute']
	# FortyMinute = db['Forty Minute']
	# OneMinute = db['One Minute']
	# RepMax = db['Rep Max']



