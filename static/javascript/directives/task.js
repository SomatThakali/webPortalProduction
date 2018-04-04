app.directive('task', function(){
  return {
    restrict: 'E',
    scope: {
      info: '='
    },
    templateUrl: '../../javascript/directives/task.html'
  }
})
