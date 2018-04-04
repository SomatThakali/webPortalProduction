app.directive('notice', function(){
  return {
    restrict: 'E',
    scope: {
      info: '='
    },
    templateUrl: '../../javascript/directives/notice.html'
  }
})
