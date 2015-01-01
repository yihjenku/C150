
import sys
import pymongo
from pymongo import MongoClient


def main(args):
	client = pymongo.MongoClient('localhost', 27017)

	db = client['MaxWatt']
	MaxWattData = db['MaxWatt1']

	# query = {'Rank': 2}

	# MaxWattData.update(query, {'$set': {'Watt 1': 869}})

	for rower in MaxWattData.find():
		print ('%s was rank %d and went %d, %d, and %d for his trials, with a high of %d and an average of %d.' % 
			(rower['Name'], rower['Rank'], rower['Watt 1'], rower['Watt 2'], rower['Watt 3'], rower['High'], rower['Average']))

	db.drop_collection('MaxWatt1')	
	client.close()

if __name__ == '__main__':
    main(sys.argv[1:])


