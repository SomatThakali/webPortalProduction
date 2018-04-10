app.directive('studiesListing', function() {
  return {
    restrict: 'E',
    scope: {
      info: '='
    },
    templateUrl: "/static/javascript/directives/studiesListing.html"
  }
});
