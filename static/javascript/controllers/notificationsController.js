app.controller('notificationsController', ['$scope', function($scope) {
  $scope.notices = [
	  {
	    description: 'Patient Revital Schechter cancelled',
	    date: "03/22/2018",
      time: "3:00 PM",
      type: "far fa-calendar-times" //for cancels
	  },
	  {
	    description: 'Jesus Mendez Cancelled',
	    date: '03/24/2018',
      time: '4:00 PM',
      type: "far fa-calendar-times" //For cancels
	  },
	  {
	    description: 'Senior Design Roast Session rescheduled',
	    date: '03/20/2018 moved to 03/25/2018',
      time: '11:00 PM moved to 2:00 PM',
      type: 'far fa-calendar-check' // for rescheduling
	  },
	  {
	    description: 'Teddy Colon updated emergency contact information',
	    date: 'edited 03/19/2018',
      time: '2:00 AM',
      type: 'fas fa-clipboard-list'//for form update
	  },
    {
      description: 'Reschedule of life after failure',
      date: '06/01/2018 moved to 06/01/2019',
      time:  '1:00 PM moved to 3:00 PM',
      type: 'far fa-calendar-check'//for rescheduling
    },
	];
}]);
