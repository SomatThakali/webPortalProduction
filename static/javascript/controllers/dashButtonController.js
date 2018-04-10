app.controller('dashButtonController', function($scope){
  $scope.cal={
    ref : "cal",
    heading : "My Calendar",
    sbClass : "panel-primary",
    backgroundClass: "primary-background",
    borderClass : "primary-border",
    icon : "fa-calendar-alt fa-5x",
    link : "patient/calendar"
  };
  $scope.prog={
    ref : "prog",
    heading : "My Progress",
    sbClass : "panel-green",
    backgroundClass: "secondary-background",
    borderClass : "secondary-border",
    icon : "fa-thumbs-up fa-5x",
    link : "patient/myprogress"
  };
  $scope.info={
    ref : "info",
    heading : "My Info",
    sbClass : "panel-yellow",
    backgroundClass: "tertiary-background",
    borderClass : "tertiary-border",
    icon : "fa-user fa-5x",
    link : "patient/information"
  };
  $scope.exer={
    ref : "exer",
    heading : "My Exercises",
    sbClass : "panel-red",
    backgroundClass: "quaternary-background",
    borderClass : "quaternary-border",
    icon : "fa-list-alt fa-5x",
    link : "patient/exercise"
  };
})
