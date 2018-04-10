app.directive('notice', function(){
  return {
    restrict: 'E',
    scope: {
      info: '='
    },
    templateUrl: '/static/javascript/directives/notice.html'
  }
})
