angular.module('BdApp', [])
    .controller('BdController', ['$scope', function ($scope) {
        $scope.templates =
            [{name: 'home.html', url: 'parts/home.html'},
                {name: 'projects.html', url: 'parts/projects.html'},
                {name: 'authors.html', url: 'parts/authors.html'},
                {name: 'sprints.html', url: 'parts/sprints.html'},
                {name: 'sprintView.html', url: 'parts/sprintView.html'},
                {name: 'task.html', url: 'parts/task.html'},
                {name: 'employees.html', url: 'parts/employees.html'},
                {name: 'employeeView.html', url: 'parts/employeeView.html'}
            ];

        $scope.projects = [{id: "1", name: "Projekt 1", person: "Adam"},
            {id: "2", name: "Projekt 2", person: "Badam"}
        ];

        $scope.sprints = [{id: "1", startDate: "12-12-2012", endDate: "12-01-2013"},
            {id: "2", startDate: "12-01-2013", endDate: "12-02-2013"}
        ];

        $scope.tasks = [{id: "1", name: "Task 1"},
            {id: "2", name: "Task 2"}
        ];

        $scope.persons = [{id: "1", name: "Adam"},
            {id: "2", name: "Badam"}
        ];

        $scope.worklogs = [{date: "10-12-2012", what: "nothing", who:"Adam", time:"1h"},
            {date: "10-12-2013", what: "compiling", who:"Badam", time:"3h"}
        ];

        $scope.employees = [{name:"Adam",position:"Junior Java Dev"},
            {name:"Badam",position:"Senior Java Dev"}
            ];

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
            console.log(val.id);
            $scope.template = $scope.templates[3];
            $scope.projectId = val;
            $scope.project = {};
            $scope.project = val;
            activateButton("projects");
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
            $scope.employee = {};
            $scope.employee = employee;
            $scope.template = $scope.templates[7];
            activateButton("employees");
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

        $scope.addProject = function () {
            console.log("Tworzenie projektu o nazwie" + $scope.projectName);
        };

        $scope.generateRaport = function () {
            console.log("Generowanie raportu sprint nr" + $scope.projectName);
        };

        $scope.viewRaport = function () {
            console.log("Oglądanie raportu nr" + $scope.projectName);
        };

        $scope.addSprint = function () {
            console.log("Tworzenie nowego sprintu");
        };

        $scope.deletePerson = function(){
            console.log("Usuwanie odpowiedzialnej osoby");
        };

        $scope.rewritePerson = function(){
            console.log("Przypisywanie wybranej osoby");
        };

        $scope.addTask = function(){
            console.log("Dodawanie zadania" +$scope.taskName);
        };

        $scope.deletePerson = function(val){
            console.log("Kasowanie osoby nr "+val);
        };

        $scope.addPerson = function(){
            console.log("Dodawanie osoby "+$scope.personName);
        };

        $scope.addWorklog=function(){
            console.log("Tworze worklog: what:"+$scope.what+"who"+$scope.who+"howMuch"+$scope.howMuch);
        };


    }]);