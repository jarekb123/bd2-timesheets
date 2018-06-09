from my_app import db
from database.models import Worklog
from apis.projects.schemas import Project, ProjectSchema, ProjectEmployeeRole, ProjectEmployeeRoleSchema, Sprint, \
    SprintSchema, Task, Worklog, Employee
from database.models import Report
from sqlalchemy import func
from flask import jsonify


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

    result = Task.query.with_entities(Employee.first_name, Employee.last_name, func.sum(Worklog.logged_hours)).filter(
        Task.sprint_id == sprint_id,
        ProjectEmployeeRole.project_id == project_id, ProjectEmployeeRole.employee_id == Employee.id,
        Worklog.task_id == Task.id, Employee.id == Worklog.employee_id).group_by(
        Worklog.employee_id).all()

    result = [[x, y, str(z)] for x, y, z in result]
    result_json = jsonify(result)
    result_str = str(result)
    report = Report(description=result_str)
    db.session.add(report)
    db.session.commit()
    return result_json


def get_sprint(project_id, sprint_id):
    sprint = Sprint.query.filter(Sprint.id == sprint_id, Sprint.project_id == project_id).first()
    return SprintSchema().jsonify(sprint)
