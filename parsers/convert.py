import csv

filename = input('Which CSV file would you like to convert to comma separated utf8: ')

try:
    with open(filename, newline='', encoding='iso8859_2') as csvfile:
        freader = csv.reader(csvfile, delimiter=';')
        # Find in the CSV file the rows maching all the key/value pairs
        outfilename = filename[0:-4] + '-utf8.csv'
        outlines = 0
        with open(outfilename, 'w', encoding='utf8') as csvoutfile:
            fwriter = csv.writer(csvoutfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for row in freader:
                fwriter.writerow(row)
                outlines += 1

        print('Finished writing %d lines to "%s"' % (outlines, outfilename))
        
except FileNotFoundError as e:
    print('There was an issue processing the file:', str(e))
