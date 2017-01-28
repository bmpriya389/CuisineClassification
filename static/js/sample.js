var feedMeApp = angular.module('feedMe',[]);

feedMeApp.directive('summary', function(){
  return {
    restrict: 'A',
    replace: false,
    scope: {
      summary: '='
    },
    link: function(scope, elem, attrs){
      // console.log('directive: call to load pie1');
      scope.summary();
    }
  }
});

feedMeApp.controller('recipeCtrl', function($scope, $http){
      $scope.ingredQuant = [];
      $scope.directions = [];
      $scope.measures = ['tsp','tbsp', 'fl oz', 'gill', 'cup', 'pint', 'quart', 'gallon', 'ml', 'litres'];
      $scope.predicted = "";
      $scope.predictValues = [];
      $scope.predict = function(){
        $http({
            method: 'POST',
            url: '/predict',
            data: {
              ingreds : 
              $scope.ingredQuant.map(
                function(ingred) { 
                  return ingred.Ingredient;
                }
              )
            }
          }).then(function(response){
            var result= response.data;
            if(typeof result != 'string'){
              $scope.predicted = result[0].predicted;
              result.shift();
              $scope.predictValues = result;
            }
            else
              $scope.predicted = '';
          },
          function(error){
            console.log(error)
          })
          
      }

      $scope.ingredientCheck = function(){
        $scope.ingredQuant.push({"Ingredient": $scope.teo_ingredient, "Quantity": $scope.teo_quantity, "Measure": $scope.selectedMeasure});
        $scope.predict();
        $scope.teo_ingredient = '';
        $scope.teo_quantity = '';     
      };

      $scope.deleteIngred = function(x, $index){
        $scope.ingredQuant.splice($index, 1);
        $scope.predict();

      };

      $scope.addDirections = function(){
        $scope.directions.push($scope.teo_direction);
        $scope.teo_direction = '';
      };

      $scope.deleteDirection = function(y, $index){
        $scope.directions.splice($index, 1);
      };

      var teoPie = function(place, data){

        var width = 600;
        var height = 400;
        var radius = d3.min([width, height])/2;
        var color =  d3.scaleOrdinal(d3.schemeCategory20b);    
        var legendRect = 10;
        var legendSpacing = 4;

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

          var legend = svg.selectAll('.legend')
                      .data(color.domain())
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
                .text(function(d) { return d; });  

      };

      $scope.pieChart = function(){
        console.log(typeof $scope.predictValues);
        teoPie('#cuisineChart', $scope.predictValues);
      };

    }
    );