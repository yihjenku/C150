# ************************************************************
# Name: Yih-Jen Ku
# UNI: yak2110
# Date: 12/2/14
# File Name: RowingCalculator.py
#
# This program calculates percentages and makes graphs. 
# ************************************************************
import pygal
# def splitCalc(time, distance):     
    
def RMAverage(squat, deadlift):
    return (squat + deadlift)/2

def percentCalc(athleteValue, olympicValue):
    return round((athleteValue/float(olympicValue)), 4)
    
def plotRadar(Name, percent40, percent1, percentRM, percentMaxWatt):
    radar_chart = pygal.Radar()
    radar_chart.title = Name
    radar_chart.x_labels = ['40 Minute', '1 Minute', '1 Rep Max', 'Max Watt']
    radar_chart.add('Testing Battery 1', [percent40, percent1, percentRM, percentMaxWatt])
    radar_chart.add('Olympic Standard', [1, 1, 1, 1])
    # radar_chart.render()
    radar_chart.render_to_file(Name + '.svg')
    # radar_chart.savefig('radar_chart.png')
# def displayStats():
    
