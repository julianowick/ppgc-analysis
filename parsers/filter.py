import csv

filename = input('Which CSV file would you like to filter: ')

try:
    with open(filename, newline='', encoding='iso8859_2') as csvfile:
        freader = csv.reader(csvfile, delimiter=';')
        headers = next(freader) # Read just the first line (headers)

        pairs = []
        keepgoing = 'y'
        while(keepgoing.lower() == 'y'):
            print('Header options are:', str(headers))

            key = input('Which header would you like to filter: ')
            if key not in headers:
                print('Invalid header, please choose again!')
                continue

            value = input('Which value would you like to use for your filter: ')
            pairs.append({'key': headers.index(key), 'value': value})
            keepgoing = input('Do you need to include one more filter? (y/n)')

        # Find in the CSV file the rows maching all the key/value pairs
        outfilename = filename[0:-4] + '-filtered.csv'
        outlines = 0
        with open(outfilename, 'w', newline='', encoding='iso8859_2') as csvoutfile:
            fwriter = csv.writer(csvoutfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            for row in freader:
                fullmatch = True
                for pair in pairs:
                    if row[pair['key']] != pair['value']:
                        fullmatch = False
                        break
                    
                if fullmatch == True:
                    fwriter.writerow(row)
                    outlines += 1

        print('Finished writing %d lines to "%s"' % (outlines, outfilename))
        
except FileNotFoundError as e:
    print('There was an issue processing the file:', str(e))
