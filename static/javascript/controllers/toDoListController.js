app.controller('toDoListController', ['$scope', function($scope) {
  $scope.tasks = [
	  {
	    task: 'Send out form to Revital Schechter',
	    date: "03/20/2018"
	  },
	  {
	    task: 'Remind Michael Gerber to exercise at home',
	    date: '03/22/2018'
	  },
	  {
	    task: 'Reschedule meeting with Dr. Wang',
	    date: '03/24/2018'
	  },
	  {
	    task: 'Send out form to Teddy Colon',
	    date: '03/25/2018'
	  },
    {
      task: 'Find the meaning to life',
      date: '04/20/2018'
    },
    {
      task: 'Argue thesis points with colleagues at the water fountain',
      date: '04/21/2018'
    }

	];
}]);
