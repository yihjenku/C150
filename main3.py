def main():
    """Creates a dictionary of sentiments with respective values for each word"""
    sents = {}
    file_in = open('sentiments.csv', 'rU')
    # Properly formats each entry by getting rid of unnecessary spaces
    # and quotation marks.
    # Citation: http://stackoverflow.com/questions/20305907
    reader = csv.reader(file_in, delimiter=',', skipinitialspace = True)
    for line in reader:
        key = line[0]
        value = float(line[1])
        sents[key] = value
    print sents