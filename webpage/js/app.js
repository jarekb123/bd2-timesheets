angular.module('BdApp', [])
    .controller('BdController', ['$scope','$http', function ($scope,$http) {
        $scope.templates =
            [{name: 'home.html', url: 'pages/home.html'},
                {name: 'projects.html', url: 'pages/projects.html'},
                {name: 'authors.html', url: 'pages/authors.html'},
                {name: 'sprints.html', url: 'pages/sprints.html'},
                {name: 'sprintView.html', url: 'pages/sprintView.html'},
                {name: 'task.html', url: 'pages/task.html'},
                {name: 'employees.html', url: 'pages/employees.html'},
                {name: 'employeeView.html', url: 'pages/employeeView.html'}
            ];

        $scope.projects = [{id: "1", name: "Projekt 1", person: "Adam"},
            {id: "2", name: "Projekt 2", person: "Badam"}
        ];

        $scope.project=[{}]

        $scope.sprints = [{id: "1", startDate: "12-12-2012", endDate: "12-01-2013"},
            {id: "2", startDate: "12-01-2013", endDate: "12-02-2013"}
        ];

        $scope.tasks = [{id: "1", name: "Task 1"},
            {id: "2", name: "Task 2"}
        ];

        $scope.persons = [{id: "1", name: "Adam"},
            {id: "2", name: "Badam"}
        ];

        $scope.worklogs = [{date: "10-12-2012", what: "nothing", who: "Adam", time: "1h"},
            {date: "10-12-2013", what: "compiling", who: "Badam", time: "3h"}
        ];

        $scope.items = [{
            id: 1,
            label: 'Pracownik 1',
        }, {
            id: 2,
            label: 'Pracownik 2',
        }];

        $scope.homeButton = function () {
            $scope.template = $scope.templates[0];
            activateButton("home");
        };
        $scope.homeButton();

        $scope.projectsButton = function () {
            $scope.template = $scope.templates[1];
            activateButton("projects");
        };

        $scope.authorsButton = function () {
            $scope.template = $scope.templates[2];
            activateButton("authors");

        };

        $scope.sprintsButton = function (val) {
            var req = {
                method: 'GET',
                url: 'http://localhost:5000/projects/'+val.id,
                headers: {
                    'Content-Type': 'json/application'
                }
            };
            $scope.projectID=val.id;
            $http(req).then(function (request) {
                console.log("success with sprints");
                console.log(request.data);
                $scope.project = request.data;
                var req = {
                    method: 'GET',
                    url: 'http://localhost:5000/projects/'+val.id+"/sprints",
                    headers: {
                        'Content-Type': 'json/application'
                    }
                };
                $http(req).then(function (request) {
                    console.log("success with sprints");
                    console.log(request.data);
                    $scope.sprints=request.data;
                    $scope.template = $scope.templates[3];
                },function(request){
                    console.log("failed sprints")
                });
                activateButton("projects");
            }, function () {
                console.log("failed projects")
            });
        };

        $scope.sprintViewButton = function (val) {
            console.log(val.id);
            $scope.sprintId = {};
            $scope.sprintId = val;
            $scope.template = $scope.templates[4];
            activateButton("projects");
        };

        $scope.taskViewButton = function (id) {
            console.log(id);
            $scope.taskID=id;
            $scope.template = $scope.templates[5];
            activateButton("projects");
        };

        $scope.employeesButton = function () {
            console.log();
            $scope.template = $scope.templates[6];
            activateButton("employees");
        };

        $scope.employeeViewButton = function (employee) {
            console.log(employee.id);
            var req = {
                    method: 'GET',
                    url: 'http://localhost:5000/employees/'+employee.id,
                    headers: {
                        'Content-Type': 'json/application'
                    }
                };
            $http(req).then(function (request) {
                console.log("success with employee");
                console.log(request.data);
                $scope.employeeChosen = request.data;
                $scope.template = $scope.templates[7];
                activateButton("employees");

            }, function () {
                console.log("failed")
            });

        };

        function activateButton(buttonName) {
            $scope.projectsActive = "";
            $scope.employeesActive = "";
            $scope.authorsActive = "";
            $scope.homeActive = "";
            if (buttonName == "projects") {
                $scope.projectsActive = "active";

            }

            if (buttonName == "authors") {
                $scope.authorsActive = "active";
            }

            if (buttonName == "employees") {
                $scope.employeesActive = "active";
            }

            if (buttonName == "home") {
                $scope.homeActive = "active";
            }
        }



        $scope.generateRaport = function () {
            console.log("Generowanie raportu sprint nr" + $scope.projectName);
        };

        $scope.viewRaport = function () {
            console.log("Oglądanie raportu nr" + $scope.projectName);
        };

        $scope.addSprint = function (startSprintTime, finishSprintTime) {
            var startDate = (new Date(startSprintTime)).toISOString().split("T")[0];
            var finishDate = (new Date(finishSprintTime)).toISOString().split("T")[0];

            var json = {
                start_time:startDate,
                finishDate:finishDate
            };
            var req = {
                method: 'POST',
                url: 'http://localhost:5000/projects/'+$scope.projectID+"/sprints",
                headers: {
                    'Content-Type': 'json/application'
                },
                data:json
            };
            $http(req).then(function (request) {
                console.log("added project");
                $scope.fetchProjects();

            }, function () {
                console.log("failed")
            });
        };

        $scope.deletePerson = function () {
            console.log("Usuwanie odpowiedzialnej osoby");
        };

        $scope.rewritePerson = function (chosenBoss) {
            console.log("Przypisywanie wybranej osoby"+chosenBoss.id);

            var json={
                employee_id:chosenBoss.id,
                employee_role_id:"1",
                rate:"1000"
            };
            console.log(json);
        };

        $scope.addTask = function () {
            console.log("Dodawanie zadania" + $scope.taskName);
        };

        $scope.deletePerson = function (val) {
            console.log("Kasowanie osoby nr " + val);
            var json={
                employeeId: val,
                taskId: $scope.taskID
            };
            console.log(json);

        };

        $scope.addPerson = function (newEmployee) {
            console.log("Dodawanie osoby " + newEmployee.id);
            var json={
                employeeId: newEmployee.id,
                taskId: $scope.taskID
            };
            console.log(json);
        };

        $scope.addWorklog = function (what, workLogEmployee, howMuch,workDate) {
            var workTime = (new Date(workDate)).toISOString().split("T")[0];

            var json = {
                employee_id: workLogEmployee.id,
                task_id: $scope.taskID,
                description: what,
                work_date: workTime,
                logged_hours: howMuch
            };
            console.log(json);
        };

        $scope.addProject = function (projectName,projectDescription, projectBudget, startTime,finishTime) {
            console.log("Tworzenie projektu o nazwie"+projectName);
            var json = {
                name: projectName,
                description: projectDescription,
                budget: projectBudget,
                start_time: startTime,
                finish_time: finishTime
            };
            console.log(json);
            var req = {
                method: 'POST',
                url: 'http://localhost:5000/projects/',
                headers: {
                    'Content-Type': 'json/application'
                },
                data:{name: projectName,
                description: projectDescription.toUTCString(),
                budget: 200.0,
                start_time: startTime.toUTCString(),
                finish_time: finishTime}
            };
            $http(req).then(function (request) {
                console.log("added project");
                $scope.fetchProjects();

            }, function () {
                console.log("failed")
            });
        };
        $scope.fetchEmployees=function(){
            var req = {
                method: 'GET',
                url: 'http://localhost:5000/employees/',
                headers: {
                    'Content-Type': 'json/application'
                }
            };
            $http(req).then(function (request) {
                console.log("fetched employees");
                $scope.employees = request.data;

            }, function () {
                console.log("failed")
            });
        };
        $scope.fetchProjects=function(){
            var req = {
                method: 'GET',
                url: 'http://localhost:5000/projects/',
                headers: {
                    'Content-Type': 'json/application'
                }
            };

            $http(req).then(function (request) {
                console.log("fetched projects");
                $scope.projects = request.data;
            }, function () {
                console.log("failed")
            });
        };

        $scope.fetchEmployees();
        $scope.fetchProjects();
    }]);