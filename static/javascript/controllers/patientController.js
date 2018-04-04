app.controller('patientController', ['$scope', 'filterFilter', function patientController($scope, filterFilter) {
  $scope.patients = [{
    id: 1,
    firstName: "John",
    lastName: "D.",
    age: "50",
  }, {
    id: 2,
    firstName: "Jane",
    lastName: "D.",
    age: "50",
  }, {
    id: 3,
    firstName: "Kevin",
    lastName: "C.",
    age: "50",
  }, {
    id: 4,
    firstName: "Teddy",
    lastName: "C.",
    age: "50",
  }, {
    id: 5,
    firstName: "Revital",
    lastName: "S.",
    age: "50",
  }];

  $scope.selected = [];


  $scope.exist = function(item) {
    return $scope.selected.indexOf(item) > -1;
  }

  //function to manage selected items
  $scope.toggleSelection = function(item) {
    var idx = $scope.selected.indexOf(item);
    if (idx > -1) {
      $scope.selected.splice(idx, 1);
    } else {
      $scope.selected.push(item);
    }
  };
  //function to select all
  $scope.checkAll = function() {
    if ($scope.selectAll) {
      angular.forEach($scope.patients, function(item) {
        idx = $scope.selected.indexOf(item);
        if (idx >= 0) {
          return true;
        } else {
          $scope.selected.push(item);
        }
      })
    } else {
      $scope.selected = [];
    }
  };
}]);