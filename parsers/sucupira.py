import csv
import json
import operator
import sys
from unidecode import unidecode

def export_graph(authorsfilename, papersfilename, outputfilename):
    with open(authorsfilename, newline='', encoding='utf8') as csvauthors, open(papersfilename, newline='', encoding='utf8') as csvpapers:
        papers = {}
        all_areas = []
        all_lines = []
        freader = csv.reader(csvpapers, delimiter=',')
        for row in freader:
            # Skip headers
            if row[0] == 'CD_PROGRAMA_IES':
                # Relevant data in csvpapers
                id_prod = row.index('ID_ADD_PRODUCAO_INTELECTUAL')
                year = row.index('AN_BASE')
                nm_area = row.index('NM_AREA_CONCENTRACAO')
                nm_line = row.index('NM_LINHA_PESQUISA')
                nm_type = row.index('NM_SUBTIPO_PRODUCAO') # journal, conference, etc.
                continue

            # Some line names start with LINHA
            if row[nm_line].startswith('LINHA '):
                line = row[nm_line][6:]
            else:
                line = row[nm_line]

            papers[row[id_prod]] = {
                'year': row[year],
                'area': unidecode(row[nm_area]),
                'line': unidecode(line),
                'type': unidecode(row[nm_type]),
                'authors': []
            }
            # Create a list of unique areas
            if papers[row[id_prod]]['area'] not in all_areas:
                all_areas.append(papers[row[id_prod]]['area'])
            # Create a list of unique lines
            if papers[row[id_prod]]['line'] not in all_lines:
                all_lines.append(papers[row[id_prod]]['line'])

        authors = {}
        freader = csv.reader(csvauthors, delimiter=',')
        author_id = 1
        for row in freader:
            # Skip headers
            if row[0] == 'AN_BASE':
                id_prod = row.index('ID_ADD_PRODUCAO_INTELECTUAL')
                nm_author = row.index('NM_AUTOR') # author's name
                tp_author = row.index('TP_AUTOR') # professor, student, external
                nm_country = row.index('NM_PAIS') # origin country
                continue
            
            author = unidecode(row[nm_author])
            paper = row[id_prod]
            if author in authors: # existing author
                # add paper to author
                authors[author]['papers'].append(paper)
                # add area/line to author if doesn't exist
                if papers[paper]['area'] != '':
                    if papers[paper]['area'] not in authors[author]['areas']:
                        authors[author]['areas'][papers[paper]['area']] = 1 # add area of paper
                    else:
                        authors[author]['areas'][papers[paper]['area']] += 1 # increment area count
                if papers[paper]['line'] != '':
                    if papers[paper]['line'] not in authors[author]['lines']:
                        authors[author]['lines'][papers[paper]['line']] = 1 # add line of paper
                    else:
                        authors[author]['lines'][papers[paper]['line']] += 1 # increment line count
                    
                # add type to author if doesn't exist
                if row[tp_author] != '-': # avoid adding "empty" types
                    if row[tp_author] not in authors[author]['types']:
                        authors[author]['types'][row[tp_author]] = papers[paper]['year'] # add type of author
                    elif papers[paper]['year'] > authors[author]['types'][row[tp_author]]: 
                        authors[author]['types'][row[tp_author]] = papers[paper]['year'] # update year of apearance

            else: # new author found
                authors[author] = {
                    'id': author_id,
                    'papers': [paper], 
                    'types': {unidecode(row[tp_author]): papers[paper]['year']}, # year of apearance of this type
                    'areas': {papers[paper]['area']: 1}, # areas counter
                    'lines': {papers[paper]['line']: 1}, # lines counter
                    'country': nm_country
                }
                author_id += 1
            
            papers[paper]['authors'].append(author)

        coauthors = {} # Co-authors dict (sets with ordered pairs of co-authors)
        links = [] # Actual links of the graph based on the co-authors list
        nodes = [] # Each author is a node
        for author in authors:
            # Find main type (most recent)
            authors[author]['type'] = max(authors[author]['types'], key=authors[author]['types'].get)

            # Groups: professor [1], student [2], alumni [3], posdoc [4], external/other [5]
            if authors[author]['type'] == 'DOCENTE':
                group = 1
            elif authors[author]['type'] == 'DISCENTE':
                group = 2
            elif authors[author]['type'] == 'EGRESSO':
                group = 2
            elif authors[author]['type'] == 'POS-DOC':
                group = 2
            else:
                group = 3

            authors[author]['group'] = group
            authors[author]['area'] = max(authors[author]['areas'], key=authors[author]['areas'].get) # main area
            authors[author]['line'] = max(authors[author]['lines'], key=authors[author]['lines'].get) # main area
            size = len(authors[author]['papers'])
            # Convert areas and lines from dict to list of dicts
            node_areas = []
            for area in authors[author]['areas']:
                node_areas.append({'area_name': area, 'area_id': all_areas.index(area) + 1, 'count': authors[author]['areas'][area]})
            node_lines = []
            for line in authors[author]['lines']:
                node_lines.append({'line_name': line, 'line_id': all_lines.index(line) + 1, 'count': authors[author]['lines'][line]})
            node = {
                'id': authors[author]['id'],
                'label': author,
                'group_id': group,
                'group_name': authors[author]['type'],
                'size': size,
                'area_id': all_areas.index(authors[author]['area']) + 1,
                'area_name': authors[author]['area'],
                'areas': node_areas,
                'line_id': all_lines.index(authors[author]['line']) + 1,
                'line_name': authors[author]['line'],
                'lines': node_lines,
                'country': authors[author]['country']
            }
            # Add node with attached information to the nodes list
            nodes.append(node)

            # Create coauthor associations
            for paper in authors[author]['papers']:
                for coauthor in papers[paper]['authors']:
                    if coauthor != author: # Avoid adding the own author to the co-author list
                        pair = str(sorted({author, coauthor})) # Always in aphabetical order
                        if pair not in coauthors: # Avoid duplicating co-author pairs
                            link = {
                                'source': authors[author]['id'],
                                'source_label': author, 
                                'target': authors[coauthor]['id'], 
                                'target_label': coauthor, 
                                'value': 1
                            }
                            coauthors[pair] = link # Record the link association
                            links.append(link)
                        else:
                            # increment the 'value' with the publication count
                            coauthors[pair]['value'] += 1

        # Highlight links between areas differently
        for i in range(len(links)):
            if authors[links[i]['source_label']]['area'] != "" and authors[links[i]['target_label']]['area'] != "" and authors[links[i]['source_label']]['area'] != authors[links[i]['target_label']]['area']:
                links[i]['interarea'] = True
            else:
                links[i]['interarea'] = False
                
            if authors[links[i]['source_label']]['line'] != "" and authors[links[i]['target_label']]['line'] != "" and authors[links[i]['source_label']]['line'] != authors[links[i]['target_label']]['line']:
                links[i]['interline'] = True
            else:
                links[i]['interline'] = False

            # Temporarily removed
            #relationship = {authors[links[i]['source']]['group'], authors[links[i]['target']]['group']}
            #if relationship == {1, 1}: # Link between professors
            #    links[i]['type'] = 1
            #elif relationship == {2, 2}: # Link between students
            #    links[i]['type'] = 2
            #elif relationship == {3, 3}: # Link between externals
            #    links[i]['type'] = 3
            #elif relationship == {1, 2}: # Link between professor and student
            #    links[i]['type'] = 4
            #elif relationship == {1, 3}: # Link between professor and external
            #    links[i]['type'] = 5
            #elif relationship == {2, 3}: # Link between student and external
            #    links[i]['type'] = 6

        data = {'nodes': nodes, 'links': links}
        with open(outputfilename, 'w') as f:
            json.dump(data, f, indent=4)

# when used via comand line
if __name__ == "__main__":
    # accepts exactly 3 arguments (authorsfilename, papersfilename, outputfilename)
    if len(sys.argv) == 4:
        authorsfilename = sys.argv[1]
        papersfilename = sys.argv[2]
        outputfilename = sys.argv[3]
    else:
        authorsfilename = input('Inform the authors CSV filename: ')
        papersfilename = input('Inform the papers CSV filename: ')
        outputfilename = input('Inform output json filename: ')

