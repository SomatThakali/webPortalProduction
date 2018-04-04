app.directive('dashButton',function(){
  return {
    restrict: 'E',
    scope: {
      ref: '=ref'
    },
    templateUrl: '/static/javascript/directives/dashButton.html'
  };
});
