app.directive('exerciseListing', function(){
  return {
    restrict: 'E',
    scope: {
      info: '='
    },
    templateUrl: '../../javascript/directives/exerciseListing.html'
  }
})
