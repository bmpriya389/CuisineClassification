      var teoPie = function(place, data){

        var width = 600;
        var height = 400;
        var radius = d3.min([width, height])/2;
        var color =  d3.scaleOrdinal(d3.schemeCategory20b);    
        var legendRect = 10;
        var legendSpacing = 4;
        d3.select("svg").remove();
          var arc = d3.arc().outerRadius(radius-20).innerRadius(0);

          var pie = d3.pie().
                      value(function(d){
                          return d.posterior;
                      }).
                      sort(null);

          var svg = d3.select(place).
                      append("svg").
                      attr("width", width).
                      attr("height", height).
                      append("g").
                      attr("transform", "translate(" + radius + "," + radius + ")");

          var path = svg.selectAll('path').
                      data(pie(data)).
                      enter().
                      append('path').
                      attr('d', arc).
                      attr('fill', function(d,i){
                          return color(d.data.cuisine);
                      }).
                      attr('text', function(d,i){
                          return d.data.cuisine;
                      });

        var colors = color.domain();

          var legend = svg.selectAll('.legend')
                      .data(colors)
                      .enter()
                      .append('g')
                      .attr('class','legend')
                      .attr("transform", function(d,i){ 
                          var height = legendRect + legendSpacing;
                          var offset =  height * color.domain().length;
                          var horz = -2 * legendRect + radius + 20; 
                          var vert = i * height - offset + 150;
                          return 'translate(' + horz + ',' + vert + ')';
                      });

          legend.append('rect')
                .attr('width', legendRect)
                .attr('height', legendRect)
                .style('fill', color)
                .style('stroke', color);


          legend.append('text')
                .attr('x', legendRect + legendSpacing)
                .attr('y', legendRect - legendSpacing)
                .text(function(d) { return String(d+ ', ' + data[colors.indexOf(d)].posterior.toFixed(4) + ' %'); });  

      };