app.directive('task', function(){
  return {
    restrict: 'E',
    scope: {
      info: '='
    },
    templateUrl: '/static/javascript/directives/task.html'
  }
})
