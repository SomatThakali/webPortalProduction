app.directive('exerciseListing', function(){
  return {
    restrict: 'E',
    scope: {
      info: '='
    },
    templateUrl: '/static/javascript/directives/exerciseListing.html'
  }
})
