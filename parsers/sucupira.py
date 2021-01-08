import csv
import json
import operator

authorsfilename = input('Inform the authors CSV filename: ')
papersfilename = input('Inform the papers CSV filename: ')
outputfilename = input('Inform output json filename: ')

with open(authorsfilename, newline='', encoding='utf8') as csvauthors, open(papersfilename, newline='', encoding='utf8') as csvpapers:
    papers = {}
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

        papers[row[id_prod]] = {
            'year': row[year],
            'area': row[nm_area],
            'line': line,
            'type': row[nm_type],
            'authors': []
        }

    authors = {}
    freader = csv.reader(csvauthors, delimiter=',')
    for row in freader:
        # Skip headers
        if row[0] == 'AN_BASE':
            id_prod = row.index('ID_ADD_PRODUCAO_INTELECTUAL')
            nm_author = row.index('NM_AUTOR') # author's name
            tp_author = row.index('TP_AUTOR') # professor, student, external
            continue
        
        author = row[nm_author]
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
                    authors[author]['types'][row[tp_author]] = 1 # add type of author
                else:
                    authors[author]['types'][row[tp_author]] += 1 # increment type count

        else: # new author found
            authors[author] = {
                'papers': [paper], 
                'types': {row[tp_author]: 1}, # types counter
                'areas': {papers[paper]['area']: 1}, # areas counter
                'lines': {papers[paper]['line']: 1} # lines counter
            }
        
        papers[paper]['authors'].append(author)

    coauthors = {} # Co-authors dict (sets with ordered pairs of co-authors)
    links = [] # Actual links of the graph based on the co-authors list
    nodes = [] # Each author is a node
    for author in authors:
        # Find main type
        authors[author]['type'] = max(authors[author]['types'], key=authors[author]['types'].get)

        # Groups: professor [1], student [2], alumni [3], posdoc [4], external/other [5]
        if authors[author]['type'] == 'DOCENTE':
            group = 1
        elif authors[author]['type'] == 'DISCENTE':
            group = 2
        elif authors[author]['type'] == 'EGRESSO':
            group = 3
        elif authors[author]['type'] == 'PÓS-DOC':
            group = 4
        else:
            group = 5

        authors[author]['group'] = group
        authors[author]['area'] = max(authors[author]['areas'], key=authors[author]['areas'].get), # main area
        authors[author]['line'] = max(authors[author]['lines'], key=authors[author]['lines'].get), # main area
        size = len(authors[author]['papers'])
        node = {
            'id': author,
            'group': group,
            'group_name': authors[author]['type'],
            'size': size,
            'area': authors[author]['area'],
            'areas': authors[author]['areas'],
            'line': authors[author]['line'],
            'lines': authors[author]['lines']
        }
        # Add node with attached information to the nodes list
        nodes.append(node)

        # Create coauthor associations
        for paper in authors[author]['papers']:
            for coauthor in papers[paper]['authors']:
                if coauthor != author: # Avoid adding the own author to the co-author list
                    pair = str(sorted({author, coauthor})) # Always in aphabetical order
                    if pair not in coauthors: # Avoid duplicating co-author pairs
                        link = {'source': author, 'target': coauthor, 'value': 1}
                        coauthors[pair] = link # Record the link association
                        links.append(link)
                    else:
                        # increment the 'value' with the publication count
                        coauthors[pair]['value'] += 1

    # Highlight links between areas differently
    for i in range(len(links)):
        if authors[links[i]['source']]['area'] != "" and authors[links[i]['target']]['area'] != "" and authors[links[i]['source']]['area'] != authors[links[i]['target']]['area']:
            links[i]['interarea'] = True
        else:
            links[i]['interarea'] = False
            
        if authors[links[i]['source']]['line'] != "" and authors[links[i]['target']]['line'] != "" and authors[links[i]['source']]['line'] != authors[links[i]['target']]['line']:
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

