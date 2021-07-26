import csv
import sys

def filter_file(inputfilename, key, value, args, outputfilename):
    try:
        with open(inputfilename, newline='', encoding='iso8859_1') as csvfile:
            freader = csv.reader(csvfile, delimiter=';')
            headers = next(freader) # Read just the first line (headers)

            pairs = []
            keepgoing = 'y'
            while(keepgoing.lower() == 'y'):
                if not args:
                    print('Header options are:', str(headers))
                    key = input('Which header would you like to filter: ')

                if key not in headers:
                    if args:
                        exit()
                    print('Invalid header, please choose again!')
                    continue

                if not args:
                    value = input('Which value would you like to use for your filter: ')
                    keepgoing = input('Do you need to include one more filter (y/n)? ')
                else:
                    keepgoing = 'n'

                pairs.append({'key': headers.index(key), 'value': value})

            if not args:
                outputfilename = inputfilename[0:-4] + '-filtered.csv'
                ofn = input(f'Which output file name would you like (suggested: {outputfilename}): ')
                if ofn:
                    outputfilename = ofn

            # Find in the CSV file the rows maching all the key/value pairs
            outlines = 0
            with open(outputfilename, 'w', newline='', encoding='utf8') as csvoutfile:
                fwriter = csv.writer(csvoutfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                fwriter.writerow(headers) # Write headers into the destination file
                for row in freader:
                    fullmatch = True
                    for pair in pairs:
                        if row[pair['key']] != pair['value']:
                            fullmatch = False
                            break
                        
                    if fullmatch == True:
                        fwriter.writerow(row)
                        outlines += 1

            print('Finished writing %d lines to "%s"' % (outlines, outputfilename))
            
    except FileNotFoundError as e:
        print('There was an issue processing the file:', str(e))

# when used via comand line
if __name__ == "__main__":
    # accepts exactly 4 arguments (inputfilename, header, filter, outputfilename)
    if len(sys.argv) == 5:
        inputfilename = sys.argv[1]
        key = sys.argv[2]
        value = sys.argv[3]
        outputfilename = sys.argv[4]
        args = True
    else:
        args = False
        inputfilename = input('Which CSV file would you like to filter: ')
        key = None
        value = None
        outputfilename = None

    filter_file(inputfilename, key, value, args, outputfilename)