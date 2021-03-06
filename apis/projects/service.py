from my_app import db
from database.models import Worklog
from apis.projects.schemas import Project, ProjectSchema, ProjectEmployeeRole, ProjectEmployeeRoleSchema, Sprint, \
    SprintSchema, Task, Worklog, Employee, TaskSchema, EmployeeSchema, WorklogSchemaSimple, ReportSchema
from database.models import Report, EmployeeRole, t_Employee_task
from sqlalchemy import func
from flask import jsonify
from ast import literal_eval

def get_all_projects():
    """
    Get all projects
    """
    return Project.query.all()


def add_project(project):
    """
    Add new project

    :param project: Project to add
    :return: Project if added, None otherwise
    """
    db.session.add(project)
    db.session.flush()
    if project.id:
        db.session.commit()
        return project


def update_project(project_json, id):
    """
    Updates particular project

    :param project: Project to update
    :param id: An ID of a project
    :return: Updated project
    """
    project = Project.query.get(id)
    if project is None:
        return {'error': 'No such project'}, 404
    project = ProjectSchema.load(project_json, instance=project).data
    db.session.add(project)
    db.session.commit()
    return ProjectSchema.jsonify(project)


def delete_project(project_id):
    """
    Deletes a project

    :param project_id: An ID of a project
    :return: Operation status message
    """
    rows_deleted = Project.query.filter_by(id=project_id).delete()
    if rows_deleted:
        db.session.commit()
        return {'status': f'Project {project_id} deleted correctly'}, 200
    else:
        return {'error': f'Project {project_id} not exists'}, 404


def add_employee_to_project(project_id, employee_role):
    """
    Adds employee's role to particular project

    :param project_id: An ID of a project
    :param employee_role: POST Payload
    :return Added employee's role data object
    """
    employee_role = ProjectEmployeeRole(
        project_id=project_id,
        employee_id=employee_role['employee_id'],
        employee_role_id=employee_role['employee_role_id'],
        rate=employee_role['rate']
    )
    db.session.add(employee_role)
    db.session.commit()

    return ProjectEmployeeRole.query.filter_by(
        project_id=employee_role.project_id,
        employee_id=employee_role.employee_id) \
        .first()


def delete_employee(project_id, employee_id):
    """ Deletes employee from project

    :param project_id: An ID of a project
    :param employee_id: An ID of an employee
    :return: Operation status message
    """
    rowsDeleted = ProjectEmployeeRole.query.filter_by(employee_id=employee_id, project_id=project_id).delete()
    if not rowsDeleted:
        return {'status': 'Employee: {} not found in Project: {}'.format(employee_id, project_id)}, 404

    db.session.commit()
    return {'status': 'Employee: {} deleted correctly from Project: {}'.format(employee_id, project_id)}, 200


def get_sprints(project_id):
    """Shows project sprints
    :param project_id: An ID of a project
    :return: Project sprints"""

    sprints = Sprint.query.filter_by(project_id=project_id).all()
    return SprintSchema(many=True).jsonify(sprints)


def add_sprint(project_id, sprint_data):
    """Add new sprint to project if there isnt one already
    :param project_id: An ID of a project
    :param sprint_data: new sprint data
    :return Operation status"""
    sprint = SprintSchema().load(data=sprint_data).data
    result = Sprint.query.filter(Sprint.project_id == project_id,
                                 Sprint.finish_time is None or Sprint.finish_time >= sprint.start_time).all()
    if result:
        return {'status': 'Another sprint already in progress'}, 409

    sprintObj = Sprint(project_id=project_id, start_time=sprint.start_time, finish_time=sprint.finish_time)
    db.session.add(sprintObj)
    db.session.commit()
    return SprintSchema().jsonify(sprintObj)


def get_sprint_report(project_id, sprint_id):
    """Get report for sprint
    :param sprint_id: A ID of sprint
    :return Sprint report"""

    result = Report.query.with_entities(Report.description).filter(Report.sprint_id == sprint_id).first()

    if result:
        result = literal_eval(result[0])
        return jsonify(result)

    result = Task.query.with_entities(Employee.first_name, Employee.last_name, func.sum(Worklog.logged_hours)).filter(
        Task.sprint_id == sprint_id,
        ProjectEmployeeRole.project_id == project_id, ProjectEmployeeRole.employee_id == Employee.id,
        Worklog.task_id == Task.id, Employee.id == Worklog.employee_id).group_by(
        Worklog.employee_id).all()

    result = [[x, y, str(z)] for x, y, z in result]
    result_str = str(result)
    report = Report(sprint_id=sprint_id, description=result_str)
    db.session.add(report)
    db.session.commit()

    report = Report.query.filter(Report.sprint_id == sprint_id).first()
    return jsonify(result)


def get_sprint(project_id, sprint_id):
    sprint = Sprint.query.filter(Sprint.id == sprint_id, Sprint.project_id == project_id).first()
    return SprintSchema().jsonify(sprint)


def create_task(sprint_id, task_data):
    """Add new task to project if there isnt one already
    :param sprint_id: An ID of a task
    :param task_data: new task data
    :return Operation status"""
    task = TaskSchema().load(data=task_data).data

    taskObj = Task(sprint_id=sprint_id, description=task.description, stage_id=task_data['stage_id'])

    db.session.add(taskObj)
    db.session.flush()
    db.session.commit()
    return TaskSchema().jsonify(taskObj)


def get_tasks(sprint_id):
    tasks = Task.query.filter_by(sprint_id=sprint_id).all()
    return TaskSchema(many=True).jsonify(tasks)


def get_task_employees(task_id):
    employees = Employee.query.join(Task.employee).filter(Task.id == task_id).all()
    return EmployeeSchema(many=True).jsonify(employees)


def get_task_worklog(task_id):
    worklog = Worklog.query.with_entities(Employee.id, Employee.first_name, Employee.last_name, Worklog.logged_hours,
                                          Worklog.creation_time, Worklog.description, Worklog.work_date).filter(
        Worklog.task_id == task_id, Worklog.employee_id == Employee.id).all()
    return jsonify(worklog)


def add_employee_task(employee_task, task):
    statement = t_Employee_task.insert().values(employee_id=employee_task['employee_id'], task_id=task)
    db.session.execute(statement)
    return db.session.commit()


def delete_employee_task(employee_task, task):
    row = Task.query.filter(Task.id == task).first()
    for i, x in enumerate(row.employee):
        if x.id == employee_task['employee_id']:
            del row.employee[i]
            return db.session.commit()
    return 'Employee or task doesnt exist'
