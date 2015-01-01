# ************************************************************
# Name: Yih-Jen Ku
# UNI: yak2110
# Date: 12/2/14
# File Name: main.py
#
# This program tests the rowing calculator. 
# ************************************************************
import RowingCalculator as r

def main():
    Name = raw_input('Enter the name of the rower: ')
    # 40 Minute Test Total Distance
    FortyMinTD = input('Enter the 40 Minute Test Total Distance: ')
    # 1 Minute Test Total Distance
    OneMinTD = input('Enter the 1 Minute Test Total Distance: ')
    # Squat 1 Rep Max Value
    SquatRM = input('Enter the Squat 1RM Value: ')
    # Deadlift 1 Rep Max Value
    DeadliftRM = input('Enter the Deadlift 1RM Value: ')
    # Max Wattage Test Value
    MaxWatt = input('Enter the Max Watt value: ')
    # Rower's Weight
    Weight = input('Enter the weight of the rower: ')
    
    # Olympic level constants
    OlympicFortyTD = 11881
    OlympicOneTD = 375
    OlympicMaxWatt = 1100
    Weight *= 2
    RMAvg = r.RMAverage(SquatRM, DeadliftRM)
    
    # Calculate percentages
    percentForty = r.percentCalc(FortyMinTD, OlympicFortyTD)
    print percentForty
    percentOne = r.percentCalc(OneMinTD, OlympicOneTD)
    print percentOne
    percentRM = r.percentCalc(RMAvg, Weight)
    print percentRM
    percentMaxWatt = r.percentCalc(MaxWatt, OlympicMaxWatt)
    print percentMaxWatt
    
    r.plotRadar(Name, percentForty, percentOne, percentRM, percentMaxWatt)
    
main()