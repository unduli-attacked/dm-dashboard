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

        $scope.killLeg = function(goddessName, cost){
            for (let goddess of $scope.data.goddesses){
                if (goddess.name == goddessName){
                    goddess.leg_action_rem -= cost;
                }
            }
        }
    }
]);
})();