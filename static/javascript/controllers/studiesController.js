app.controller('studiesController', ['$scope', function($scope) {
  $scope.studies = [{
    nameOfStudy: "Study #1",
    content: "This study is about A",
    requirements: "Participants must be X",
    link: "collap1"
  }, {
    nameOfStudy: "Study #2",
    content: "This study is about B",
    requirements: "Participants must be Y",
    link: "collap2"
  }, {
    nameOfStudy: "Study #3",
    content: "This study is about C",
    requirements: "Participants must be Z",
    link: "collap3"
  }, {
    nameOfStudy: "Study #4",
    content: "This study is about D",
    requirements: "Participants must be XYZ",
    link: "collap4"
  }];

}]);
