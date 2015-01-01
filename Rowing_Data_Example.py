
import sys
import pymongo

Example_Data = [
	{
		'Rank': 2,
		'Name': 'Bellesheim',
		'Watt 1': 859,
		'Watt 2': 847,
		'Watt 3': 842,
		'High': 859,
		'Average': 849
	},
	{
		'Rank': 4,
		'Name': 'Ptucha',
		'Watt 1': 800,
		'Watt 2': 812,
		'Watt 3': 800,
		'High': 812,
		'Average': 804
	},
	{
		'Rank': 12,
		'Name': 'Blair',
		'Watt 1': 718,
		'Watt 2': 739,
		'Watt 3': 752,
		'High': 752,
		'Average': 736
	},
	{
		'Rank': 17,
		'Name': 'Whitlock',
		'Watt 1': 711,
		'Watt 2': 0,
		'Watt 3': 735,
		'High': 735,
		'Average': 723
	}
]

def main(args):
	client = pymongo.MongoClient('localhost', 27017)

	db = client['MaxWatt']
	MaxWattData = db['MaxWatt1']

	MaxWattData.insert(Example_Data)

	query = {'Rank': 2}

	MaxWattData.update(query, {'$set': {'Watt 1': 869}})

	for rower in MaxWattData.find():
		print rower	
		# print ('%s was rank %d and went %d, %d, and %d for his trials, with a high of %d and an average of %d.' % 
		#	(rower['Name'], rower['Rank'], rower['Watt 1'], rower['Watt 2'], rower['Watt 3'], rower['High'], rower['Average']))

	db.drop_collection('MaxWatt1')	
	client.close()

if __name__ == '__main__':
    main(sys.argv[1:])
