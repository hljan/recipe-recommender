// functions
function openTab(tabName) {

    var tabLinks = document.getElementsByClassName("tablink");

    for (i = 0; i < tabLinks.length; i++) {
        if (tabLinks[i].value === tabName) {
            tabLinks[i].disabled = "true";
            if (tabName === "recipe" || tabName === "contentBased" || tabName === "collaborative") {
                document.getElementById("tab_btn_cnt").style.display = "block";
                document.getElementById("tab_btn_col").style.display = "block";
            } else if (tabName === "ingredient") {
                document.getElementById("tab_btn_ing_cfm").style.display = "block";
            }
        }
    }
}

function draw_graph_q1(nodes, links, div_id) {
    // define graph size
    var margin = {left: 130, top: 20, right: 100, bottom: 100},
        width = window.innerWidth - margin.left - margin.right,
        height = window.innerHeight - margin.top - margin.bottom;

    var force = d3.forceSimulation()
        .nodes(d3.values(nodes))
        .force("link", d3.forceLink(links).distance(300))
        .force('center', d3.forceCenter(width / 2 + margin.left, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-3000))
        .alphaTarget(1)
        .on("tick", function (e) {
            // add the curves
            path.attr("d", function (d) {
                // fix the root node
                var dx = d.target.x - d.source.x,
                    dy = d.target.y - d.source.y,
                    dr = Math.sqrt(dx * dx + dy * dy);
                return "M" +
                    d.source.x + "," +
                    d.source.y + "A" +
                    dr + "," + dr + " 0 0,1 " +
                    d.target.x + "," +
                    d.target.y;
            });
            node.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
        });

    var svg = d3.select(div_id)
        .append("svg")
        .attr("width", width + margin.left)
        .attr("height", height + margin.top)
        .attr("transform", "translate(" + margin.left + ",0)");

    // define the links
    var path = svg.append("g")
        .selectAll("path")
        .data(links)
        .enter()
        .append("path")
        .attr("class", 'nodeLink');

    // define tooltip
    var tooltip = d3.tip()
        .attr('class', 'd3-tooltip')
        .offset([-10, 5])
        .html(function (d) {
            var details = "";
            if (d.id === 0) {
                details = d.name;
            } else {
                details = "Recipe Name: " + d.name;
            }

            return details;
        });
    svg.call(tooltip);

    // define the nodes
    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter()
        .append("g")
        .attr("class", "node")
        .on("dblclick", dblclicked_q1)
        .on('mouseover', tooltip.show)
        .on('mouseout', tooltip.hide);

    // add the nodes
    node.append("circle")
        .attr("r", function (d) {
            if (d.id === 0) {
                return 50;
            } else {
                return 70;
            }
        })
        .style("fill", function (d) {
            if (d.id === 0) {
                return d3.interpolateRdYlBu(0.45);
            } else {
                return d3.interpolateRdYlBu(0.75);
            }
        });

    // add the node labels
    node.append("text")
        .attr("dx", -40)
        .attr("dy", 0)
        .attr("transform", "translate(0, -5)")
        .style("font-weight", 800)
        .text(function (d) {
            return d.name;
        })
        .call(wrap, 100);

};

// double click action
function dblclicked_q1(d) {
    var recipe_id = d.id;
    if (recipe_id !== 0) {
        var user_id = window.location.pathname.split('/')[2],
            recipe_name = d.name,
            recipe = recipe_id + "&" + recipe_name;
        url = encodeURI("/visualSearch/" + user_id + "/recipe_info/" + recipe);

        window.location.assign(url);
    }
};

// wrap node text
function wrap(text, width) {
    text.each(function () {
        var text = d3.select(this),
            text_str = text.text(),
            limit = 35;

        // limit the size of the text
        if (width < 100) {
            if (text_str.slice(-1) === "*") {
                text_str = text_str.substr(0, text_str.length - 1);
                limit = 17;
            }
        }

        if (text_str.length > limit) {
            text_str = text_str.substr(0, limit) + "..."
        }

        var word,
            words = text_str.split(/\s+/).reverse(),
            line = [],
            lineNumber = 0,
            lineHeight = 1.1, // ems
            x = text.attr("x"),
            y = text.attr("y"),
            dy = 0,
            tspan = text.text(null)
                .append("tspan")
                .attr("x", x)
                .attr("y", y)
                .attr("dy", dy + "em");
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > width) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                tspan = text.append("tspan")
                    .attr("x", x - 40)
                    .attr("y", y - 1)
                    .attr("dy", ++lineNumber * lineHeight + dy + "em")
                    .text(word);
            }
        }
    });
};

function draw_graph_q4(nodes, links, div_id) {
    // define graph size
    var margin = {left: 130, top: 20, right: 100, bottom: 100},
        width = window.innerWidth - margin.left - margin.right,
        height = window.innerHeight - margin.top - margin.bottom;

    var force = d3.forceSimulation()
        .nodes(d3.values(nodes))
        .force("link", d3.forceLink(links).distance(300))
        .force('center', d3.forceCenter(width / 2 + margin.left, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-3000))
        .alphaTarget(1)
        .on("tick", function (e) {
            // add the curves
            path.attr("d", function (d) {
                // fix the root node
                var dx = d.target.x - d.source.x,
                    dy = d.target.y - d.source.y,
                    dr = Math.sqrt(dx * dx + dy * dy);
                return "M" +
                    d.source.x + "," +
                    d.source.y + "A" +
                    dr + "," + dr + " 0 0,1 " +
                    d.target.x + "," +
                    d.target.y;
            });
            node.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
        });

    var svg = d3.select(div_id)
        .append("svg")
        .attr("width", width + margin.left)
        .attr("height", height + margin.top)
        .attr("transform", "translate(" + margin.left + ",0)");

    // define the links
    var path = svg.append("g")
        .selectAll("path")
        .data(links)
        .enter()
        .append("path")
        .attr("class", 'nodeLink');

    // define tooltip
    var tooltip = d3.tip()
        .attr('class', 'd3-tooltip')
        .offset([-10, 5])
        .html(function (d) {
            var details = "";
            if (d.id === 0) {
                details = d.name;
            } else {
                details = "Ingredient Name: " + d.name;
            }

            return details;
        });
    svg.call(tooltip);

    // define the nodes
    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter()
        .append("g")
        .attr("class", "node")
        .on("click", clicked_q4)
        .on('mouseover', tooltip.show)
        .on('mouseout', tooltip.hide);

    // add the nodes
    node.append("circle")
        .attr("r", function (d) {
            if (d.id === 0) {
                return 50;
            } else {
                return 70;
            }
        })
        .style("fill", function (d) {
            if (d.id === 0) {
                return d3.interpolateRdYlBu(0.45);
            } else {
                return d3.interpolateRdYlBu(0.75);
            }
        });

    // add the node labels
    node.append("text")
        .attr("dx", -40)
        .attr("dy", 0)
        .attr("transform", "translate(0, -5)")
        .style("font-weight", 800)
        .text(function (d) {
            return d.name
        })
        .call(wrap, 100);

};

// click action
function clicked_q4(d) {
    if (d.id !== 0) {
        var cfm_btn = document.getElementById("tab_btn_ing_cfm");
        cfm_btn.disabled = false;
    }

    d3.select(this).select("text").transition()
        .duration(750)
        .text(function (d) {
            if (d.id === 0) {
                return d.name;
            } else {
                return "*" + d.name;
            }
        });
};

function draw_graph_q5(nodes, links, div_id) {
    // define graph size
    var margin = {left: 130, top: 20, right: 100, bottom: 100},
        width = window.innerWidth - margin.left - margin.right,
        height = window.innerHeight - margin.top - margin.bottom;

    var force = d3.forceSimulation()
        .nodes(d3.values(nodes))
        .force("link", d3.forceLink(links).distance(300))
        .force('center', d3.forceCenter(width / 2 + margin.left, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-3000))
        .alphaTarget(1)
        .on("tick", function (e) {
            // add the curves
            path.attr("d", function (d) {
                // fix the root node
                var dx = d.target.x - d.source.x,
                    dy = d.target.y - d.source.y,
                    dr = Math.sqrt(dx * dx + dy * dy);
                return "M" +
                    d.source.x + "," +
                    d.source.y + "A" +
                    dr + "," + dr + " 0 0,1 " +
                    d.target.x + "," +
                    d.target.y;
            });
            node.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
        });

    var svg = d3.select(div_id)
        .append("svg")
        .attr("width", width + margin.left)
        .attr("height", height + margin.top)
        .attr("transform", "translate(" + margin.left + ",0)");

    // define the links
    var path = svg.append("g")
        .selectAll("path")
        .data(links)
        .enter()
        .append("path")
        .attr("class", 'nodeLink');

    // define tooltip
    var tooltip = d3.tip()
        .attr('class', 'd3-tooltip')
        .offset([-10, 5])
        .html(function (d) {
            var details = "";
            if (d.id === 0) {
                details = "Recipe Name: " + d.name +
                    "<br />Alternative Ingredients: " + "bla bla bla";
            } else {
                details = "Ingredient Name: " + d.name;
            }

            return details;
        });
    svg.call(tooltip);

    // define the nodes
    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter()
        .append("g")
        .attr("class", "node")
        .on("dblclick", dblclicked_q5)
        .on('mouseover', tooltip.show)
        .on('mouseout', tooltip.hide);

    // add the nodes
    node.append("circle")
        .attr("r", function (d) {
            if (d.id === 0) {
                return 50;
            } else {
                return 70;
            }
        })
        .style("fill", function (d) {
            if (d.id === 0) {
                return d3.interpolateRdYlBu(0.45);
            } else {
                return d3.interpolateRdYlBu(0.75);
            }
        });

    // add the node labels
    node.append("text")
        .attr("dx", -40)
        .attr("dy", 0)
        .attr("transform", "translate(0, -5)")
        .style("font-weight", 800)
        .text(function (d) {
            if (d.id === 0) {
                return d.name + "*";
            } else {
                return d.name
            }
        })
        .call(wrap, 90);

};

// double click action
function dblclicked_q5(d) {
    var recipe_id = d.id;
    if (recipe_id === 0) {
        var user_id = window.location.pathname.split('/')[2],
            recipe = window.location.pathname.split('/')[4];

        recipe = recipe.replace("%26", "&");
        url = "/main/" + user_id + "/recipe_details/" + recipe;

        window.location.assign(url);
    }
};

function draw_graph_q7(nodes, links, div_id) {
    // define graph size
    var margin = {left: 130, top: 20, right: 100, bottom: 100},
        width = window.innerWidth - margin.left - margin.right,
        height = window.innerHeight - margin.top - margin.bottom;

    var force = d3.forceSimulation()
        .nodes(d3.values(nodes))
        .force("link", d3.forceLink(links).distance(300))
        .force('center', d3.forceCenter(width / 2 + margin.left, height / 2))
        .force("x", d3.forceX())
        .force("y", d3.forceY())
        .force("charge", d3.forceManyBody().strength(-3000))
        .alphaTarget(1)
        .on("tick", function (e) {
            // add the curves
            path.attr("d", function (d) {
                // fix the root node
                var dx = d.target.x - d.source.x,
                    dy = d.target.y - d.source.y,
                    dr = Math.sqrt(dx * dx + dy * dy);
                return "M" +
                    d.source.x + "," +
                    d.source.y + "A" +
                    dr + "," + dr + " 0 0,1 " +
                    d.target.x + "," +
                    d.target.y;
            });
            node.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
        });

    var svg = d3.select(div_id)
        .append("svg")
        .attr("width", width + margin.left)
        .attr("height", height + margin.top)
        .attr("transform", "translate(" + margin.left + ",0)");

    // define the links
    var path = svg.append("g")
        .selectAll("path")
        .data(links)
        .enter()
        .append("path")
        .attr("class", 'nodeLink');

    // define tooltip
    var tooltip = d3.tip()
        .attr('class', 'd3-tooltip')
        .offset([-10, 5])
        .html(function (d) {
            var details = "";
            if (d.id === 0) {
                details = "Recipe Name: " + d.name +
                    "<br />Alternative Ingredients: " + "bla bla bla";
            } else {
                details = "User ID: " + d.id +
                    "<br />User " + d.name;
            }

            return details;
        });
    svg.call(tooltip);

    // define the nodes
    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter()
        .append("g")
        .attr("class", "node")
        .on("dblclick", dblclicked_q5)
        .on('mouseover', tooltip.show)
        .on('mouseout', tooltip.hide);

    // add the nodes
    node.append("circle")
        .attr("r", function (d) {
            if (d.id === 0) {
                return 50;
            } else {
                return 70;
            }
        })
        .style("fill", function (d) {
            if (d.id === 0) {
                return d3.interpolateRdYlBu(0.45);
            } else {
                return d3.interpolateRdYlBu(0.75);
            }
        });

    // add the node labels
    node.append("text")
        .attr("dx", -40)
        .attr("dy", 0)
        .attr("transform", "translate(0, -5)")
        .style("font-weight", 800)
        .text(function (d) {
            if (d.id === 0) {
                return d.name + "*";
            } else {
                return d.name
            }
        })
        .call(wrap, 90);

};