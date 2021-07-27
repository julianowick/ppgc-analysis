import csv
import sys

def normalize_names(inputfilename, outputfilename, args):
    try:
        with open(inputfilename, newline='', encoding='utf8') as csvfile:
            freader = csv.reader(csvfile, delimiter=',')
            headers = next(freader) # Read just the first line (headers)
            # CSV file must have these columns (prod-autor file)
            id_rows = [
                headers.index('ID_PESSOA_DISCENTE'),
                headers.index('ID_PESSOA_DOCENTE'),
                # headers.index('ID_PARTICIPANTE_PPG_IES'),
                headers.index('ID_PESSOA_PART_EXTERNO'),
                headers.index('ID_PESSOA_POS_DOC'),
                headers.index('ID_PESSOA_EGRESSO')
            ]
            nm_author = headers.index('NM_AUTOR') # author's name

            # Find in the CSV file the rows maching any of the id rows
            outlines = 0
            ids_found = {}
            with open(outputfilename, 'w', newline='', encoding='utf8') as csvoutfile:
                fwriter = csv.writer(csvoutfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                fwriter.writerow(headers) # Write headers into the destination file
                for row in freader:
                    valid_id = False
                    for id in id_rows:
                        # consider only non-null IDs
                        if len(row[id]) > 0:
                            valid_id = True
                            # someone with this ID already exists
                            if row[id] in ids_found:
                                if row[nm_author] != ids_found[row[id]]:
                                    print(f"Found different names for ID {row[id]} ({headers[id]})")
                                    print(f"{row[nm_author]} -> {ids_found[row[id]]}")
                                    row[nm_author] = ids_found[row[id]]
                                    break
                            else:
                                ids_found[row[id]] = row[nm_author]
                    if not valid_id:
                        pass
                        #print(f"WARNING: IDless person person found: {row[nm_author]}")

                    fwriter.writerow(row)
                    outlines += 1

            print('Finished writing %d lines to "%s"' % (outlines, outputfilename))
            
    except FileNotFoundError as e:
        print('There was an issue processing the file:', str(e))

# when used via comand line
if __name__ == "__main__":
    # accepts exactly 2 arguments (inputfilename, outputfilename)
    if len(sys.argv) == 3:
        inputfilename = sys.argv[1]
        outputfilename = sys.argv[2]
        args = True
    else:
        args = False
        inputfilename = input('Which CSV file would you like to normalize: ')
        outputfilename = inputfilename[0:-4] + '-normalized.csv'
        ofn = input(f'Which output file name would you like (suggested: {outputfilename}): ')
        if ofn:
            outputfilename = ofn

    normalize_names(inputfilename, outputfilename, args)