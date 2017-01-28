var feedMeApp = angular.module('feedMe',[]);

feedMeApp.directive('summary', function(){
  return {
    restrict: 'A',
    
    link: function(scope, elem, attrs){
        scope.$watch('predictValues', function(){
          scope.pieChart();
        });
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
          });

          
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

      $scope.pieChart = function(){
        teoPie('#cuisineChart', $scope.predictValues);
      };

    }
    );