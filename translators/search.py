import pymongo

def searchRower(name):
	
	client = pymongo.MongoClient('localhost', 27017)
	db = client['C150']
	db.drop_collection(name)
	RowerDB = db[name]
	RowerData = []
	
	Tests = ['Max Watt', 'Twenty Minute', 'One Minute', 'Forty Minute', 'Rep Max']

	# Put all test items specific to one rower into a new collection
	for test in Tests:
		database = db[test]
		i = 1
		for rower in database.find({'Name': name}).sort([('Year', pymongo.ASCENDING), \
														('Month', pymongo.ASCENDING), \
														('Day', pymongo.ASCENDING), \
														('Rank', pymongo.ASCENDING)] ):
			# print rower
			RowerData.append(rower)
			query = {'Day': rower['Day'], \
					'Month': rower['Month'], \
					'Year': rower['Year'], \
					'Name': rower['Name'], \
					'Test': rower['Test']}
			update = rower
			update['index'] = i
			RowerDB.update(query, update, True)
			i += 1

	rower_items = {'items': RowerData}
	return rower_items

	client.close()

def searchTest(test):
	client = pymongo.MongoClient('localhost', 27017)
	db = client['C150']
	RowerDB = db[test]
	RowerData = []
	Dates = []
	rower_items = {}
	result_dicts = []
	# Put all test items specific to one test into a new collection
	for rower in RowerDB.find({'Test': test}).sort([('Year', pymongo.ASCENDING), \
													('Month', pymongo.ASCENDING), \
													('Day', pymongo.ASCENDING), \
													('Rank', pymongo.ASCENDING)] ):
		if rower['Date'] not in Dates:
			Dates.append(rower['Date'])
		RowerData.append(rower)

	i = 1
	for date in Dates:
		temp = []
		for rower in RowerData:
			if rower['Date'] == date:
				temp.append(rower)
		temp_dict = {}
		temp_dict['rowers'] = temp
		temp_dict['date'] = date
		result_dicts.append(temp_dict)
		i += 1

	rower_items['items'] = result_dicts
	return rower_items

	client.close()