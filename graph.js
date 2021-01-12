//Constants for the SVG
var width = 1200, height = 800;
//Global simulation variable
var simulation;
//Gloal color scheme for nodes
var color = d3.scaleOrdinal(d3.schemeCategory10);
//Global SVG drawing
var svg;
//Dataset configuration from UFL
var dataset = window.location.search.slice(1);
if(dataset == ""){
    dataset = "2017-2020";
}

d3.json('data/graph-PPGC-UFRGS-' + dataset + '.json').then(function(data){

	simulation = d3.forceSimulation(data.nodes)
	    .force("link", d3.forceLink(data.links).id(function(d) { return d.id; })) 
    	.force("charge", d3.forceManyBody())
        .force("x", d3.forceX())
        .force("y", d3.forceY());
    	//.force("center", d3.forceCenter(width / 2, height / 2));

	//simulation.force("link").links(data.links);

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
	    .data(data.links)
	    .enter().append("line")
    	//.attr("class", "links")
        .attr("class", function(d) { if(d.interarea) { return "links interarea"; }else{ return "links"; }})
    	.attr("stroke-width", function(d) { return d.value });

	var node = g.append("g")
    	.selectAll("g")
	    .data(data.nodes)
    	.enter().append("g")
    	.attr("class", "nodes");

	var circles = node.append("circle").on("click", function(d){fill_node_info(d)})
    	.attr("r", function(d) { return node_size(d.size); })
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
	    //update circle positions each tick of the simulation 
    	node
			.attr("transform", function(d) {
          		return "translate(" + d.x + "," + d.y + ")";
	        })
        	//.attr("cx", function(d) { return d.x; })
	        //.attr("cy", function(d) { return d.y; });
        
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
});

function node_size(n){
    return (n/2)+4;
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
    //console.log(node);
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
    var example_sizes = [20, 10, 5, 1];
    var sizes_svg = d3.select("#legend-sizes").append("svg")
        .attr("height", 150)
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
	console.log(enabledGroups);
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
