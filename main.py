import csv 
import sys
import MaxWatt as mw
import RepMax as rm
import OneMinute as om
import TwentyMinute as tm
import FortyMinute as fm
import search as s
import GraphOlympic as go

def main(args):

	choice = menu()
	if (choice == 1):
		mw.readMaxWatt(args[0])
	elif (choice == 2):
		rm.readRepMax(args[0])
	elif (choice == 3):
		om.readOneMinute(args[0])
	elif (choice == 4):
		tm.readTwentyMinute(args[0])
	elif (choice == 5):
		fm.readFortyMinute(args[0])
	elif (choice == 6):
		s.search(args[0])
	elif (choice == 7):
		go.graph(args[0])
	else:
		print 'Goodbye!'

def menu():
	print '(1) Max Watt'
	print '(2) 1 Rep Max'
	print '(3) One Minute'
	print '(4) Twenty Minute'
	print '(5) Forty Minute'
	print '(6) Search Rower'
	print '(7) Make Olympian Graph'
	choice = input('Enter an option: ')
	return choice

if __name__ == "__main__":
   main(sys.argv[1:])