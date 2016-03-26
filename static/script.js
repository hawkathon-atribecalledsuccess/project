var myApp = angular.module('doorMgrApp',[]);

myApp.controller('doorMgrCtrl', ['$scope', '$http', function($scope, $http) {
	$scope.urlbase = "http://52.90.193.208/api";
	$scope.doors = [];
	$scope.doorSelected = false;
	$scope.selectedDoor = {"doorName":"", "location":"", "people":[]};
	$scope.getDoors = function(){
		$http({method: 'POST', 
			   url: $scope.urlbase + '/getDoors'
			  }).then(
			function(response){
				$scope.doors = response.data.response;
				console.log(response)
				$scope.getUsers()
			}
		)
	}
	$scope.getDoors()
	$scope.getDoor = function(doorName){
		$http({method: 'POST', 
			   url: $scope.urlbase + '/getDoor',
			   data: {"doorName": doorName}
			  }).then(
			function(response){
				$scope.selectedDoor = response.data.response.Item;
				console.log(response);
				$scope.doorSelected = true;
			}
		)
	}
	$scope.removeDoor = function(doorName){
		$http({method: 'DELETE', 
			   url: $scope.urlbase + '/removeDoor',
			   headers: {"Content-Type": "application/json;charset=utf-8"},
			   data: {"doorName": doorName}
			  }).then(
			function(response){
				console.log(response);
				$scope.refresh()
				$scope.doorSelected = false;
			}
		)
	}
	$scope.addDoor = function(doorName, location, people){
		$http({method: 'POST', 
			  url: $scope.urlbase + '/addDoor',
			  data: {"doorName":doorName, "location":location, "people":people}
			  }).then(
			function(response){
				console.log(response);
				$scope.getDoors()
			}
		)
	}
	$scope.submitAddDoor = function(){
		$scope.addDoor($scope.addDoorFields.doorName, $scope.addDoorFields.location, ['+1' + $scope.addDoorFields.user]);
	}
	
	
	$scope.users = [];
	$scope.userSelected = false;
	$scope.selectedUser = {"phoneNumber":"", "name":"", "auth":""};
	$scope.getUsers = function(){
		$http({method: 'POST', 
			   url: $scope.urlbase + '/getPeople'
			  }).then(
			function(response){
				$scope.users = response.data.response;
				console.log(response)
			}
		)
	}
	$scope.getUsers()
	$scope.getPerson = function(phoneNumber){
		$http({method: 'POST', 
			   url: $scope.urlbase + '/getPerson',
			   data: {"phoneNumber": phoneNumber}
			  }).then(
			function(response){
				$scope.selectedUser = response.data.response.Item;
				console.log(response);
				$scope.doorsByPerson(phoneNumber)
				$scope.userSelected = true;
			}
		)
	}
	$scope.doorsByPerson = function(phoneNumber){
		$http({method: 'POST', 
			   url: $scope.urlbase + '/doorsByPerson',
			   data: {"phoneNumber": phoneNumber}
			  }).then(
			function(response){
				$scope.selectedUser.doors = response.data.response;
				console.log(response);
			}
		)
	}
	$scope.removeUser = function(phoneNumber){
		$http({method: 'DELETE', 
			   url: $scope.urlbase + '/removePerson',
			   headers: {"Content-Type": "application/json;charset=utf-8"},
			   data: {"phoneNumber": phoneNumber}
			  }).then(
			function(response){
				console.log(response);
				$scope.refresh()
				$scope.userSelected = false;
			}
		)
	}
	$scope.submitAddUser = function(){
		$scope.addUser('+1' + $scope.addUserFields.phoneNumber, $scope.addUserFields.name, 0)
	}
	
	$scope.addUser = function(phoneNumber, name, auth){
		$http({method: 'POST', 
			  url: $scope.urlbase + '/addPerson',
			  data: {"phoneNumber": phoneNumber, "name":name, "clearance":auth}
			  }).then(
			function(response){
				console.log(response);
			}
		)
	}
	$scope.addPermission = function(phoneNumber, doorName){
		$http({method: 'POST', 
			  url: $scope.urlbase + '/addPermission',
			  headers: {"Content-Type": "application/json;charset=utf-8"},
			  data: {"phoneNumber": phoneNumber, "doorName": doorName}
			  }).then(
			function(response){
				console.log(response);
				$scope.doorsByPerson(phoneNumber)
				$scope.refresh()
				$scope.getDoor(doorName)
			}
		)
	}
	$scope.removePermission = function(phoneNumber, doorName){
		$http({method: 'POST', 
			  url: $scope.urlbase + '/removePermission',
			  headers: {"Content-Type": "application/json;charset=utf-8"},
			  data: {"phoneNumber": phoneNumber, "doorName": doorName}
			  }).then(
			function(response){
				console.log(response);
				$scope.doorsByPerson(phoneNumber)
				$scope.refresh()
				$scope.getDoor(doorName)
			}
		)
	}
	$scope.refresh = function(){
		$scope.getDoors()
		$scope.getUsers()
	}
}]);