import csv 
import sys
from os import listdir
from os.path import isfile, join
from translators import MaxWatt, RepMax, OneMinute, TwentyMinute, FortyMinute, search as s, Graphics as g

def main(args):

	# Types of tests/translators
	translators = {'MaxWatt': MaxWatt, 'RepMax': RepMax, 'OneMinute': OneMinute, \
					'TwentyMinute': TwentyMinute, 'FortyMinute': FortyMinute}

	# Find all rowing data files 
	mypath = 'raw_data/'
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
	
	# Match the correct translator with the file and 
	for csv_filename in onlyfiles:
		for prefix, mod in translators.iteritems():
			if csv_filename.startswith(prefix):
				full_path = join(mypath, csv_filename)
				mod.translate(full_path)
				print 'System translating ' + full_path + '...'
				break

	print 'Done translating data! Check output file for results.'

	s.searchRower(args[0])
	s.searchTest('Max Watt')
	g.graphSplitChanges(args[0])

if __name__ == "__main__":
	main(sys.argv[1:])