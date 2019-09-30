import csv
import json

with open('../data/autores-PPGC-UFRGS-2013-2016-periodico-Sucupira.csv', newline='') as csvauthors, open('../data/papers-PPGC-UFRGS-2013-2016-periodico-Sucupira.csv', newline='') as csvpapers:
    papers = {}
    freader = csv.reader(csvpapers, dialect='excel')
    for row in freader:
        # Data in csvpapers
        # ID_ADD_PRODUCAO_INTELECTUAL [5]
        # NM_AREA_CONCENTRACAO [15]
        # NM_LINHA_PESQUISA [17]

        # Skip headers
        if row[0] == 'CD_PROGRAMA_IES':
            continue

        paper = row[5]
        papers[paper] = {'area': [row[15]], 'line': row[17], 'authors': []}

    authors = {}
    freader = csv.reader(csvauthors, dialect='excel')
    for row in freader:
        # Data in csvauthors
        # ID_ADD_PRODUCAO_INTELECTUAL [10]
        # NM_AUTOR [16]
        # TP_AUTOR [17]

        # Skip headers
        if row[0] == 'AN_BASE':
            continue
        
        author = row[16]
        paper = row[10]
        if author in authors:
            authors[author]['papers'].append(paper)
        else:
            authors[author] = {'papers': [paper], 'type': row[17]}
        
        papers[paper]['authors'].append(author)

    coauthors = [] # Co-authors list (sets with pairs of co-authors)
    links = [] # Actual links of the graph based on the co-authors list
    nodes = [] # Each author is a node
    for author in authors:
        # Groups: professor [1], student [2], External [3]
        if authors[author]['type'] == 'DOCENTE':
            group = 1
        elif authors[author]['type'] == 'DISCENTE':
            group = 2
        else:
            group = 3
        size = len(authors[author]['papers'])
        node = {'id': author, 'group': group, 'size': size} # TODO: group should be the main research area
        nodes.append(node)
        for paper in authors[author]['papers']:
            for coauthor in papers[paper]['authors']:
                if coauthor != author: # Avoid adding the own author to the co-author list
                    pair = {author, coauthor}
                    if pair not in coauthors: # Avoid duplicating co-author pairs
                        coauthors.append(pair)
                        link = {'source': author, 'target': coauthor, 'value': 1}
                        links.append(link)
                    else:
                        pass # TODO: increment here the 'value' with the publication count

    # TODO: Destacar arestas entre areas diferentes

    data = {'nodes': nodes, 'links': links}
    with open('../data/graph-PPGC-UFRGS-2013-2016-periodico-Sucupira.json', 'w') as f:
        json.dump(data, f, indent=4)

        
