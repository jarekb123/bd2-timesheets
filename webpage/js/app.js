angular.module('BdApp', [])
    .controller('BdController', ['$scope', '$http', function ($scope, $http) {
        $scope.templates =
            [{name: 'home.html', url: 'pages/home.html'},
                {name: 'projects.html', url: 'pages/projects.html'},
                {name: 'authors.html', url: 'pages/authors.html'},
                {name: 'sprints.html', url: 'pages/sprints.html'},
                {name: 'sprintView.html', url: 'pages/sprintView.html'},
                {name: 'task.html', url: 'pages/task.html'},
                {name: 'employees.html', url: 'pages/employees.html'},
                {name: 'employeeView.html', url: 'pages/employeeView.html'},
                {name: 'reports.html', url: 'pages/reports.html'}
            ];

        $scope.taskStage = ["Waiting", "In progress", "Done"];
        $scope.taskItems = [{
            id: 1,
            label: 'Waiting',
        }, {
            id: 2,
            label: 'In progress',
        },
            {
                id: 3,
                label: 'Done'
            }];
        $scope.anyReport = false;
        ////////NAVIGATION///////////////////
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


        $scope.employeesButton = function () {
            console.log();
            $scope.template = $scope.templates[6];
            activateButton("employees");
        };

        $scope.employeeViewButton = function (employee) {
            console.log(employee.id);
            var req = {
                method: 'GET',
                url: 'http://localhost:5000/employees/' + employee.id,
                headers: {
                    'Content-Type': 'json/application'
                }
            };
            $http(req).then(function (request) {
                console.log("success with employee");
                console.log(request.data);
                $scope.employeeChosen = request.data;
                var req = {
                    method: 'GET',
                    url: 'http://localhost:5000/employees/' + employee.id + '/tasks',
                    headers: {
                        'Content-Type': 'json/application'
                    }
                };
                $http(req).then(function (request) {
                    console.log('success with tasks employee');
                    $scope.employeeTasks = request.data;
                    $scope.employeeTasks.forEach(function (e) {
                        e.stage = $scope.taskStage[e.stage - 1];
                    });
                    console.log($scope.employeeTasks);
                    $scope.template = $scope.templates[7];
                    activateButton("employees");
                }, function () {
                    console.log('failed');
                });

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

////// EMPLOYEE VIEW ///////
        $scope.generateEmployeeRaport = function (month, year) {
            var req = {
                method: 'GET',
                url: 'http://localhost:5000/employees/' + $scope.employeeChosen.id + '/gen_report/' + year + '/' + month,
                headers: {
                    'Content-Type': 'json/application'
                }
            };

            $http(req).then(function (request) {
                console.log("fetched report");
                $scope.employeeReport = request.data;
                $scope.anyReport = true;
            }, function () {
                console.log("failed")
            });
        };
///////////////////// PROJECT VIEW FUNCTIONS ///////////////
        $scope.addProject = function (projectName, projectDescription, projectBudget, startTime, finishTime) {
            console.log("Tworzenie projektu o nazwie" + projectName);

            var req = {
                method: 'POST',
                url: 'http://localhost:5000/projects/',
                headers: {
                    // 'Content-Type': 'json/application'
                },
                data: {
                    name: projectName,
                    description: projectDescription,
                    budget: projectBudget,
                    start_time: startTime.toISOString(),
                    finish_time: finishTime.toISOString()

                }
            };
            $http(req).then(function (request) {
                console.log("added project");
                $scope.fetchProjects();

            }, function () {
                console.log("failed")
            });
        };
        $scope.sprintsButton = function (val) {
            var req = {
                method: 'GET',
                url: 'http://localhost:5000/projects/' + val.id,
                headers: {
                    'Content-Type': 'json/application'
                }
            };
            $scope.projectID = val.id;
            $http(req).then(function (request) {
                console.log("success with sprints");
                console.log(request.data);
                $scope.project = request.data;
                var req = {
                    method: 'GET',
                    url: 'http://localhost:5000/projects/' + val.id + "/sprints",
                    headers: {
                        'Content-Type': 'json/application'
                    }
                };
                $http(req).then(function (request) {
                    console.log("success with sprints");
                    console.log(request.data);
                    $scope.sprints = request.data;
                    var req = {
                        method: 'GET',
                        url: 'http://localhost:5000/projects/' + val.id + "/employees",
                        headers: {
                            'Content-Type': 'json/application'
                        }
                    };
                    $http(req).then(function (request) {
                        console.log("success with employees");
                        console.log(request.data);
                        $scope.projectPeople = request.data;
                        $scope.template = $scope.templates[3];
                    }, function () {

                    });


                }, function (request) {
                    console.log("failed sprints")
                });
                activateButton("projects");
            }, function () {
                console.log("failed projects")
            });
        };
/////////////// SPRINTS PAGE FUNCTIONS ///////////////////

        $scope.sprintViewButton = function (val) {
            console.log(val.id);
            $scope.sprintId = val.id;
            var req = {
                method: 'GET',
                url: 'http://localhost:5000/projects/' + $scope.projectID + '/sprints/' + val.id,
                headers: {
                    'Content-Type': 'json/application'
                }
            };
            $http(req).then(function (request) {
                console.log("success with sprint basic");
                $scope.sprint = request.data;
                var req = {
                    method: 'GET',
                    url: 'http://localhost:5000/projects/' + $scope.projectID + '/sprints/' + val.id + '/task',
                    headers: {
                        'Content-Type': 'json/application'
                    }
                };
                $http(req).then(function (request) {
                    console.log('success with sprint tasks');
                    $scope.sprintTasks = request.data;
                    $scope.sprintTasks.forEach(function (e) {
                        e.stage = $scope.taskStage[e.stage - 1];
                    });
                }, function (request) {
                    console.log('failed sprint tasks');
                });
            }, function (request) {
                console.log("failed sprint basic")
            });
            $scope.template = $scope.templates[4];
            activateButton("projects");
        };


        $scope.viewRaport = function (val) {
            console.log("Oglądanie raportu nr" + val.id);
            $scope.sprint = val;
            var req = {
                method: 'GET',
                url: 'http://localhost:5000/projects/' + $scope.projectID + '/sprints/' + $scope.sprint.id + '/report',
                headers: {}
            };

            $http(req).then(function (request) {
                console.log("fetched projects");
                console.log(request.data);
                $scope.report = request.data;
                $scope.report.forEach(function (e) {
                    e.name = e[0] + ' ' + e[1];
                    e.hours = e[2];
                });
                $scope.template = $scope.templates[8];

            }, function () {
                console.log("failed")
            });
        };

        $scope.addSprint = function (startSprintTime, finishSprintTime) {
            $scope.errorOverlapSprint = false;
            $scope.errorSprint = false;

            var json = {
                start_time: startSprintTime.toISOString(),
                finish_time: finishSprintTime.toISOString()
            };
            json = JSON.stringify(json);
            console.log(json);
            var req = {
                method: 'POST',
                url: 'http://localhost:5000/projects/1/sprints',
                headers: {},
                data: {
                    start_time: startSprintTime.toISOString(),
                    finish_time: finishSprintTime.toISOString()
                }
            };
            $http(req).then(function (request) {
                console.log("added project");
                var elem = {id: $scope.projectID};
                $scope.sprintsButton(elem);

            }, function (response) {
                console.log("failed");

                if (response.status == 409) {
                    $scope.errorOverlapSprint = true;
                } else {
                    $scope.errorSprint = true;
                }
            });
        };
        $scope.deleteProjectPerson = function (chosenPersonId) {
            var req = {
                method: 'DELETE',
                url: 'http://localhost:5000/projects/' + $scope.projectID + '/employees/' + chosenPersonId,
                headers: {}
            };
            $http(req).then(function (request) {
                console.log("deleted person");
                var elem = {id: $scope.projectID};
                $scope.sprintsButton(elem);
            }, function (request) {
                console.log("failed downloading");
            });

        };

        $scope.rewriteProjectPerson = function (chosenBoss) {

            var req = {
                method: 'POST',
                url: 'http://localhost:5000/projects/' + $scope.projectID + '/employees',
                headers: {},
                data: {
                    employee_id: chosenBoss.id,
                    employee_role_id: 1,
                    rate: "1000"
                }
            };
            $http(req).then(function (request) {
                console.log("added person");
                var elem = {id: $scope.projectID};
                $scope.sprintsButton(elem);

            }, function () {
                console.log("failed")
            });

        };

////////////// SPRINT VIEW FUNCTIONS////////////////////
        $scope.addTask = function (description, stage) {
            var req = {
                method: 'POST',
                url: 'http://localhost:5000/projects/' + $scope.projectID + '/sprints/' + $scope.sprintId + '/task',
                headers: {},
                data: {
                    description: description,
                    stage_id: stage.id,
                }
            };
            $http(req).then(function (request) {
                console.log("added task");
                var elem = {id: $scope.sprintId};
                $scope.sprintViewButton(elem);

            }, function () {
                console.log("failed")
            });

        };
        $scope.taskViewButton = function (task) {
            console.log(task);
            $scope.task = task;
            var req = {
                method: 'GET',
                url: 'http://localhost:5000/projects/' + $scope.projectID + '/sprints/' + $scope.sprint.id + '/task/' + task.id + '/worklog',
                headers: {
                    'Content-Type': 'json/application'
                }
            };

            $http(req).then(function (request) {
                console.log("fetched worklogs");
                $scope.taskWorklogs = request.data;
                var req = {
                    method: 'GET',
                    url: 'http://localhost:5000/projects/' + $scope.projectID + '/sprints/' + $scope.sprint.id + '/task/' + task.id + '/employees',
                    headers: {
                        'Content-Type': 'json/application'
                    }
                };
                $http(req).then(function (request) {
                    console.log('success task employees');
                    $scope.taskEmployees = request.data;
                }, function (request) {
                    console.log('failed');
                })
            }, function () {
                console.log("failed")
            });
            $scope.template = $scope.templates[5];
            activateButton("projects");
        };

/////// TASK VIEW FUNCTIONS/////

        $scope.deletePerson = function (val) {
            var req = {
                method: 'DELETE',
                url: 'http://localhost:5000/projects/' + $scope.projectID + '/sprints/' + $scope.sprint.id + '/task/' + $scope.task.id + '/employees',
                headers: {
                    'Content-Type': 'application/json'
                },
                data: {
                    employee_id: val.id
                }
            };
            $http(req).then(function (request) {
                console.log("deleted Person");
                $scope.taskViewButton($scope.task);

            }, function () {
                console.log("failed")
            });

        };

        $scope.addPerson = function (newEmployee) {
            var req = {
                method: 'POST',
                url: 'http://localhost:5000/projects/' + $scope.projectID + '/sprints/' + $scope.sprint.id + '/task/' + $scope.task.id + '/employees',
                headers: {},
                data: {
                    employee_id: newEmployee.id
                }
            };
            $http(req).then(function (request) {
                console.log("added persion");

                $scope.taskViewButton($scope.task);

            }, function () {
                console.log("failed")
            });

        };

        $scope.addWorklog = function (what, workLogEmployee, howMuch, workDate) {
            var date = (new Date(workDate)).toISOString().split("T")[0];
            var req = {
                method: 'POST',
                url: 'http://localhost:5000/worklog/',
                headers: {},
                data: {
                    employee_id: workLogEmployee.id,
                    task_id: $scope.task.id,
                    description: what,
                    work_date: date,
                    logged_hours: parseInt(howMuch)
                }
            };
            $http(req).then(function (request) {
                console.log("added worklog");

                $scope.taskViewButton($scope.task);

            }, function () {
                console.log("failed")
            });

        };


        ////////////// FIRST FETCHES////////////////////
        $scope.fetchEmployees = function () {
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
                $scope.items = [];

                $scope.employees.forEach(function (e) {
                    var name = e.first_name + " " + e.last_name;
                    var elem = {
                        id: e.id,
                        label: name
                    };
                    $scope.items.push(elem);

                });

            }, function () {
                console.log("failed")
            });
        };
        $scope.fetchProjects = function () {
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
    }
    ]);