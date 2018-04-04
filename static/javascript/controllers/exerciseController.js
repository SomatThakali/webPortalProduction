app.controller('exerciseController', ['$scope', function($scope) {
  $scope.exercises = [
	  {
	    heading: 'Home Exercise 1',
	    description: "This exercise is a little bit more challenging but we believe you're ready for it!",
	    link: 'Prolonged Wrist Exercises',
	  },
	  {
	    heading: 'Home Exercise 2',
	    description: 'You should try doing this exercise at least twice a week!',
	    link: 'Putty Exercises',
	  },
	  {
	    heading: 'Home Exercise 3',
	    description: 'This is a good starting exercise for you!',
	    link: 'Ulna and Radial Deviation',
	  },
	  {
	    heading: 'Home Exercise 4',
	    description: 'This will strengthen the core muscles in your wrist.',
	    link: 'Wrist Flexion',
	  }
	];
}]);
