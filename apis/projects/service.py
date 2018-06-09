from my_app import db
from apis.projects.schemas import Project, ProjectSchema, ProjectEmployeeRole, ProjectEmployeeRoleSchema
from database.models import Worklog


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
        employee_id=employee_role.employee_id)\
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
