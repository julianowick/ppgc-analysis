# ppgc-analysis
Set of scripts dedicated to analyze and visualize Brazilian publication data extracted from Sucupira open data platform. The original idea is to extract publication information and observe cooperation between research areas within a post-graduate program scientific production (papers published in journals and conferences). Cooperation, in this case, is considered in terms of co-authorship of papers. We assume that if two authors from different areas publish a paper together, they collaborate in some interdisciplinary research.

## Running Demo
There is currently a [demo of the co-authorship graph visualization running here](http://labcom.inf.ufrgs.br/~jwickboldt/ppgc-analysis/graph.html). The demo is implemented using [D3.js Force](https://github.com/d3/d3-force). 

### Graph visualization
In summary, the graph shows authors as nodes and co-authorship relations as edges. The size of a node represents the number of papers by that author in that dataset. The width of an edge represents the number of papers co-authored by the two ends of the relationship. Colors represent research areas/lines, while shapes represent author types (professors, students, externals).  

### Interactions
Clicking on a node selects it, showing relevant information on the sidebar. It also highlights all connected nodes and their edges. A second click unselects the node. Edges are also selectable, in which case the edge and both ends are highlighted, and information is shown on the sidebar. The same datasets available in the [data folder](data) are selectable from the top menu to visualize the interactions among authors from each post-graduate program. It is also possible to filter out nodes by type.

### Forces
There are three forces acting on the graph. A global force pulls all nodes to the center of the graph, that is why the overall shape of the graph tends to be round. Each node has an electrostatic charge (repulsion) with a strength proportional to its size. Meaning that large nodes will push others far away from their orbits, which prevents nodes from overlapping too much. Edges pull nodes close together with a strength proportional to their width, similar to a spring force. Therefore, authors that cooperate more frequently tend to appear close to one another in the graph.

## Main scripts

* [parsers/convert.py](parsers/convert.py): simply converts a CSV file from semicolon/iso8859_2 (default format from Sucupira) to comma/utf8 (most commonly used in other platforms).
* [parsers/filter.py](parsers/filter.py): Sucupira CSV files are very large, so this script allows you to filter the files using one or more strings for every header in the CSV file. The script can be either called with 3 arguments (input file, header, and string to match) or be used interactively. 
* [parsers/merge.py](parsers/merge.py): Sucupira exports publications in CSV files separated by type (i.e., journal and conferences), so this script allows merging any number of CSV files with identical headers. The script can be either called with 2 arguments (two CSV files to merge) or be used interactively for merging multiple files. 
* [parsers/sucupira.py](parsers/sucupira.py): given a Sucupira-formated authors CSV file (prefix "prod-autor-") and a scientific production CSV file (prefix "producao-"), this script creates a graph containing authors as vertices and co-authorship relations as edges. Both vertices and edges are populated with attributes, such as the research area, type (professor, student, external), size (publication count), and co-authorship count (for edges). The script can be either called with 3 arguments (prod-autor file, producao file, and output graph json file) or be used interactively.
* [parsers/graphml.py](parsers/graphml.py): an attempt to convert the graph into the GraphML format (might be outdated).
* [parsers/automate.sh](parsers/automate.sh): a simple script to call all the other scripts in order and automate the creation of the graph for a given post-graduate program. The script works based on the program's ID from Capes, something like 42001013004P4. See all the IDs at [Capes website](https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/programa/quantitativos/quantitativoBuscaAvancada.jsf).

## Sucupira Open Data
Every post-graduate program in Brazil is required to submit their reports to Capes, which evaluates their scientific production and publicizes this data. There are several open datasets available from Capes at https://dadosabertos.capes.gov.br/, some of which are used by this application. 
