(function () {
    'use strict';

    angular.module('CombatApp', []).controller('CombatController', ['$scope', '$log', '$http',
    function ($scope, $log, $http) {
        $scope.data = {};
        $http.post('/data').then(function(results){
            $scope.data = results.data;
        });
        $scope.subNext = function () {
            $http.post('/next_turn', $scope.data).then(function(results){
                $scope.data = results.data;
            });
        }

        $scope.subAisForm = function () {
            $http.post('/change_form', $scope.data).then(function(results){
                $scope.data = results.data;
            });
        }

        $scope.killLeg = function(cost){
            $scope.data.aisForm.leg_action_rem -= cost;
        }
    }
]);
})();