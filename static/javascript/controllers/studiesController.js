app.controller('studiesController', function patientController($scope) {
  $scope.studies = [{
    nameOfStudy: "Study 1"
  }, {
    nameOfStudy: "Study 2"
  }, {
    nameOfStudy: "Study 3"
  }];

  $scope.selected = [];


  $scope.exist = function(item) {
    return $scope.selected.indexOf(item) > -1;
  }
});