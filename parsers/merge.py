import csv
import sys

def merge_files(basefilename, otherfilename, outputfilename, args):
    try:
        with open(basefilename, newline='', encoding='utf8') as csvfile:
            basefreader = csv.reader(csvfile, delimiter=',')
            baseheaders = next(basefreader) # Read just the first line (headers)
            if not args:
                outputfilename = basefilename[0:-4] + '-merged.csv'
                ofn = input(f'Which output file name would you like (suggested: {outputfilename}): ')
                if ofn:
                    outputfilename = ofn
            # Find in the CSV file the rows maching all the key/value pairs
            outlines = 0
            with open(outputfilename, 'w', newline='', encoding='utf8') as csvoutfile:
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
                    with open(outputfilename, 'a', newline='', encoding='utf8') as csvoutfile:
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

    print('Finished writing %d lines to "%s"' % (outlines, outputfilename))

# when used via comand line
if __name__ == "__main__":
    # Accepts exactly 3 arguments (basefilename, otherfilename, outputfilename)
    if len(sys.argv) == 3:
        basefilename = sys.argv[1]
        otherfilename = sys.argv[2]
        outputfilename = sys.argv[3]
        args = True
    else:
        args = False
        basefilename = input('Which CSV file would you like to open (comma separated, utf-8): ')
        otherfilename = None
        outputfilename = None
    
    merge_files(basefilename, otherfilename, outputfilename, args)