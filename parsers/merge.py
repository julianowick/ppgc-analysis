import csv
import sys

# Accepts exactly 2 arguments (basefilename, otherfilename)
if len(sys.argv) == 3:
    basefilename = sys.argv[1]
    otherfilename = sys.argv[2]
    args = True
else:
    args = False
    basefilename = input('Which CSV file would you like to open (comma separated, utf-8): ')
try:
    with open(basefilename, newline='', encoding='utf8') as csvfile:
        basefreader = csv.reader(csvfile, delimiter=',')
        baseheaders = next(basefreader) # Read just the first line (headers)
        # Find in the CSV file the rows maching all the key/value pairs
        outfilename = basefilename[0:-4] + '-merged.csv'
        outlines = 0
        with open(outfilename, 'w', newline='', encoding='utf8') as csvoutfile:
            fwriter = csv.writer(csvoutfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            fwriter.writerow(baseheaders) # Write headers into the destination file
            for row in basefreader:
                fwriter.writerow(row)
                outlines += 1

except FileNotFoundError as e:
    print('There was an issue processing the file:', str(e))

onemorefile = 'y'
files = 1
while(onemorefile.lower() == 'y'):
    if not args:
        otherfilename = input('Which CSV file would you like to merge (comma separated, utf-8): ')
    try:
        with open(otherfilename, newline='', encoding='utf8') as csvfile:
            otherfreader = csv.reader(csvfile, delimiter=',')
            otherheaders = next(otherfreader) # Read just the first line (headers)

            if otherheaders == baseheaders: # can only merge identical CSV headers
                with open(outfilename, 'a', newline='', encoding='utf8') as csvoutfile:
                    fwriter = csv.writer(csvoutfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                    for row in otherfreader:
                        fwriter.writerow(row)
                        outlines += 1

        
    except FileNotFoundError as e:
        print('There was an issue processing the file:', str(e))

    if args:
        break
    onemorefile = input('Do you need to include one more file to merge (y/n)? ')
    files += 1

print('Finished writing %d lines to "%s"' % (outlines, outfilename))
