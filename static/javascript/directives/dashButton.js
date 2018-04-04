app.directive('dashButton',function(){
  return {
    restrict: 'E',
    scope: {
      ref: '=ref'
    },
    templateUrl: '../../javascript/directives/dashButton.html'
  };
});
