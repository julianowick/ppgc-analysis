//Constants for the SVG
var width = 1200, height = 800;
//Global simulation variable
var simulation;
//Gloal color scheme for nodes
var color = d3.scaleOrdinal(d3.schemeCategory10);
//Global SVG drawing
var svg;
//Configuration from URL
var urlsearch = new URLSearchParams(window.location.search);
var enable_professors = true;
var enable_students = true;
var enable_external = true;
if(urlsearch.get('dataset') == null){
    dataset = "2017-2020";
}else{
    dataset = urlsearch.get('dataset');
    enable_professors = urlsearch.get('professors')==null?false:true;
    enable_students = urlsearch.get('students')==null?false:true;
    enable_external = urlsearch.get('external')==null?false:true;
}

d3.json('data/graph-PPGC-UFRGS-' + dataset + '.json').then(function(data){
    // Groups enabled to display
    var enabled_groups = [];
    if (enable_professors) enabled_groups.push(1);
    if (enable_students) enabled_groups.push(2);
    if (enable_external) enabled_groups.push(3);

    // Initialize simulation with all nodes and links
    simulation = d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links).id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody().strength(function(d) { return -(d.size*12); }))
        .force("x", d3.forceX())
        .force("y", d3.forceY());
    	//.force("center", d3.forceCenter(width / 2, height / 2));

    // Filter out nodes if groups are disabled
    simulation.nodes(data.nodes.filter(function(n){ return enabled_groups.includes(n.group_id); }));
	simulation.force("link").links(data.links.filter(function(l){ return enabled_groups.includes(l.source.group_id) && enabled_groups.includes(l.target.group_id); }));

	//Append a SVG to the body of the html page. Assign this SVG as an object to svg
	svg = d3.select("#graph").append("svg")
        .attr("viewBox", [-width / 2, -height / 2, width, height]);
		//.attr("width", width)
	    //.attr("height", height);

	//add encompassing group for the zoom 
	var g = svg.append("g")
    	.attr("class", "everything");

	//draw lines for the links first
	var link = g.append("g")
	    .selectAll("line")
	    .data(simulation.force("link").links())
	    .enter().append("line")
        .on("click", function(d, i, v){ select_edge(d, i, v); })
    	//.attr("class", "links")
        .attr("class", function(d) { if(d.interarea) { return "links interarea"; }else{ return "links"; }})
    	.attr("stroke-width", function(d) { return d.value/2 }); // TODO: values are doubled, need to fix in dataset

	var node = g.append("g")
    	.selectAll("g")
	    .data(simulation.nodes())
    	.enter().append("g")
    	.attr("class", "nodes");

    // professors (group_id == 1) are circles
    node.filter(function(d){return d.group_id == 1})
        .append("circle")
        .on("click", function(d, i, v){ select_node(d, i, v); })
    	.attr("r", function(d) { return node_size(d.size); })
      	.attr("fill", function(d) { return color(d.area_id); });

    // students (group_id == 2) are squares
    node.filter(function(d){return d.group_id == 2})
        .append("rect")
        .on("click", function(d, i, v){ select_node(d, i, v); })
    	.attr("width", function(d) { return node_size(d.size)*2; })
    	.attr("height", function(d) { return node_size(d.size)*2; })
      	.attr("fill", function(d) { return color(d.area_id); });
    // others (group_id == 3) are rounded squares
    node.filter(function(d){return d.group_id == 3})
        .append("polygon")
        .on("click", function(d, i, v){ select_node(d, i, v); })
    	.attr("points", function(d) { side = node_size(d.size)*2; return "0," + side + " " + side + "," + side + " " + side/2 + ",0" ; })
      	.attr("fill", function(d) { return color(d.area_id); });
    

	var labels = node.append("text")
    	.text(function(d) {
			if (d.group_id == 1){
		        return d.label;
			}else{
				return "";
			}
    	})
      	.attr('x', 6)
      	.attr('y', 3);

	  node.append("title")
	      .text(function(d) { return d.label + " (" + d.size + ") " + "Area: " + d.area_name ; });

	//add drag capabilities  
	var drag_handler = d3.drag()
		.on("start", drag_start)
		.on("drag", drag_drag)
		.on("end", drag_end);

	drag_handler(node);

	//add zoom capabilities 
	var zoom_handler = d3.zoom()
    	.on("zoom", zoom_actions);

	zoom_handler(svg);

	//Drag functions 
	//d is the node 
	function drag_start(d) {
		if (!d3.event.active) simulation.alphaTarget(0.3).restart();
		d.fx = d.x;
		d.fy = d.y;
	}

	//make sure you can't drag the circle outside the box
	function drag_drag(d) {
		d.fx = d3.event.x;
		d.fy = d3.event.y;
	}

	function drag_end(d) {
		if (!d3.event.active) simulation.alphaTarget(0);
		d.fx = null;
		d.fy = null;
	}

	//Zoom functions 
	function zoom_actions(){
    	g.attr("transform", d3.event.transform)
	}

	simulation.on("tick", tickActions);

	function tickActions(){
	    // update circle positions each tick of the simulation 
        // professors (group_id == 1) are circles
        node.filter(function(d){return d.group_id == 1})
			.attr("transform", function(d) {
          		return "translate(" + d.x + "," + d.y + ")";
	        })
	    // update circle positions each tick of the simulation 
        // others (group_id != 1) are squares
        node.filter(function(d){return d.group_id != 1})
			.attr("transform", function(d) {
          		return "translate(" + (d.x - node_size(d.size)) + "," + (d.y - node_size(d.size)) + ")";
	        })
        
    	//update link positions 
	    //simply tells one end of the line to follow one node around
    	//and the other end of the line to follow the other node around
	    link
    	    .attr("x1", function(d) { return d.source.x; })
        	.attr("y1", function(d) { return d.source.y; })
	        .attr("x2", function(d) { return d.target.x; })
    	    .attr("y2", function(d) { return d.target.y; });
	} 
    fill_legend();
    fill_menu();
});

function node_size(n){
    return (n/3)+4;
}

function unselect_nodes(){
    d3.selectAll("line").property("style", "stroke-opacity: 0.3");
    d3.selectAll("circle, rect, polygon").property("style", "stroke-width: 1px");
}

function select_node(node, index, shapes){
    // Unselect all previously selected nodes
    unselect_nodes();
    // Increase strock width of shape
    shapes[index].style.strokeWidth = "2px";
    // Increase opacity of all incoming/outgoing links
    d3.selectAll("line").filter(function(l){ return l.source.id == node.id || l.target.id == node.id; }).property("style", "stroke-opacity: 1");
    // TODO: display labels for all co-authors
    fill_node_info(node);
}

function fill_node_info(node){
    var node_info = d3.select("#node-info")
    node_info.text(node.label + " (" + node.group_name + ")");
    node_info.append("p").text("Papers: " + node.size);
    node_info.append("h2").text("Research Areas");
    var areas_list = node_info.append("ul");
    for (var i = 0; i < node.areas.length; i++){
        areas_list.append("li").text(node.areas[i].area_name + " (" + node.areas[i].count + ")");
    }
    node_info.append("h2").text("Research Lines");
    var lines_list = node_info.append("ul");
    for (var i = 0; i < node.lines.length; i++){
        lines_list.append("li").text(node.lines[i].line_name + " (" + node.lines[i].count + ")");
    }
}

function select_edge(edge, index, shapes){
    // Unselect all previously selected nodes
    unselect_nodes();
    // Increase strock width of shape
    shapes[index].style.strokeOpacity = "1";
    // Increase opacity of all incoming/outgoing links
    d3.selectAll("circle, rect, polygon").filter(function(n){ if (n === undefined) return false; return n.id == edge.source.id || n.id == edge.target.id; }).property("style", "stroke-width: 2px");
    // TODO: display labels for source and target
    fill_edge_info(edge);
}

function fill_edge_info(edge){
    var edge_info = d3.select("#edge-info")
    edge_info.text(edge.source_label + " <-> " + edge.target_label);
    edge_info.append("p").text("Co-authored papers: " + edge.value/2); // TODO: values are doubled, need to fix in dataset
    edge_info.append("p").text("Between research areas: " + edge.interarea);
    edge_info.append("p").text("Between research lines: " + edge.interline);
}

// Fill legend wit info
function fill_legend(){
    var nodes = simulation.nodes();
	var links = simulation.force('link').links();

    // Fill graph basic info
    d3.select("#info-nodes").text(nodes.length);
    d3.select("#info-links").text(links.length);

    // Fills areas/colors array based on node information
    var all_area_id = [];
    var all_area_name = [];
    for (var i = 0; i < nodes.length; i++){
        if (all_area_id.indexOf(nodes[i].area_id) == -1){ // only unique area ids
            all_area_id.push(nodes[i].area_id);
            if (nodes[i].area_name != ""){
                all_area_name.push(nodes[i].area_name);
            }else{
                all_area_name.push("N/A");
            }
        }
    }
    var colors_svg = d3.select("#legend-colors").append("svg")
        .attr("height", 15 * all_area_id.length)
        .attr("width", 250);
    for (var i = 0; i < all_area_id.length; i++){
        var g = colors_svg.append("g");
        g.append("circle")
            .attr("r", 6)
            .attr("cx", 9)
            .attr("cy", (14*(i+1))-5)
            .attr("fill", color(all_area_id[i]));
        g.append("text")
            .attr("x", 18)
            .attr("y", 14*(i+1))
            .attr("style", "font-size: 12px")
            .text(all_area_name[i]);
    }
    // Example sizes
    var example_sizes = [30, 15, 5, 1];
    var sizes_svg = d3.select("#legend-sizes").append("svg")
        .attr("height", 90)
        .attr("width", 250);
    for (var i = 0; i < example_sizes.length; i++){
        var g = sizes_svg.append("g");
            g.append("circle")
                .attr("r", node_size(example_sizes[i]))
                .attr("cx", 20)
                .attr("cy", (20*(i+1))-5)
                .attr("fill", "#999");
            g.append("text")
                .attr("x", 40)
                .attr("y", 20*(i+1))
                .attr("style", "font-size: 12px")
                .text(example_sizes[i] + " papers");
    }
    var shapes_svg = d3.select("#legend-shapes").append("svg")
        .attr("height", 100)
        .attr("width", 250);
    var g = shapes_svg.append("g");
        g.append("circle")
            .attr("r", 10)
            .attr("cx", 18)
            .attr("cy", 12)
            .attr("fill", "#999");
        g.append("text")
            .attr("x", 40)
            .attr("y", 17)
            .attr("style", "font-size: 12px")
            .text("Professors");
        g.append("rect")
            .attr("x", 9)
            .attr("y", 30)
            .attr("width", 20)
            .attr("height", 20)
            .attr("fill", "#999");
        g.append("text")
            .attr("x", 40)
            .attr("y", 45)
            .attr("style", "font-size: 12px")
            .text("Students/Alumni/Pos-doc");
        g.append("polygon")
            .attr("points", "9,80 29,80 19,60")
            .attr("fill", "#999");
        g.append("text")
            .attr("x", 40)
            .attr("y", 75)
            .attr("style", "font-size: 12px")
            .text("External/Others");

}

function fill_menu(){
    d3.select("#enable_professors").property("checked", enable_professors);
    d3.select("#enable_students").property("checked", enable_students);
    d3.select("#enable_external").property("checked", enable_external);
    d3.select("#dataset").property("value", dataset);
}

// All groups enabled at first
var enabledGroups = [1, 2, 3];

function updateGroups(toogleGroup){
	indexGroup = enabledGroups.indexOf(toogleGroup);
	if (indexGroup < 0){ // Not found
		enabledGroups.push(toogleGroup);
	}else{
		enabledGroups.splice(indexGroup, 1);
	}
	var Snodes = svg.selectAll('.nodes');
	var Slinks = svg.selectAll('.links');

	var Fnodes = simulation.nodes();
	var Flinks = simulation.force('link').links();

	var filteredFnodes = Fnodes.filter(function(n){return enabledGroups.includes(n.group_id);});
	var filteredFlinks = Flinks.filter(function(l){return enabledGroups.includes(l.source.group_id) && enabledGroups.includes(l.target.group_id);});

	simulation.nodes(filteredFnodes);
	simulation.force('link').links(filteredFlinks);

	function nodeBind(d) { return d.id; }

	Snodes = Snodes.data(filteredFnodes, nodeBind);
	
	//var node = Snodes.enter().insert("g").attr("class", "nodes");

	//var circles = node.append("circle")
    //	.attr("r", function(d) { return (d.size/3) + 4; })
	//    .attr("fill", function(d) { return color(d.group_id); });

	//var labels = node.append("text")
    //	.text(function(d) {
    //   	//if (d.group_id == 1){
    //        	return d.id;
	//        //}else{
    //	    //    return "";
    //    	//}
    //	})
	//    .attr('x', 6)
    //	.attr('y', 3);

	//    node.append("title")
    //	    .text(function(d) { return d.id; });
	
	Snodes.exit().remove();

	function linkBind(d) { return d.source.id+d.target.id; }

	Slinks = Slinks.data(filteredFlinks, linkBind);
	
	//Slinks.enter().insert("line")
	//    	.attr("class", "links")
    //		.attr("stroke-width", 2);
	
	Slinks.exit().remove();
	
	simulation.alphaTarget(0.3).restart();
}
