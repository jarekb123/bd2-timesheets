from my_app import db


class Employee(db.Model):
    __tablename__ = 'Employee'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    job_position = db.Column(db.String(45), nullable=False)
    contract_finish_date = db.Column(db.Date)

    # tasks = db.relationship('Task', secondary='Employee_task')


class EmployeeFreetime(db.Model):
    __tablename__ = 'Employee_freetime'

    freetime_type_id = db.Column(db.ForeignKey('Freetime_type.id'), primary_key=True, nullable=False, index=True)
    employee_id = db.Column(db.ForeignKey('Employee.id'), primary_key=True, nullable=False, index=True)
    freetime_date = db.Column(db.Date, nullable=False)
    free_hours_sum = db.Column(db.Integer, nullable=False)

    employee = db.relationship('Employee')
    freetime_type = db.relationship('FreetimeType')


class EmployeeReport(db.Model):
    __tablename__ = 'Employee_report'

    employee_id = db.Column(db.ForeignKey('Employee.id'), primary_key=True, nullable=False)
    hours_sum = db.Column(db.Integer, nullable=False)
    report_sprint_id = db.Column(db.ForeignKey('Report.sprint_id'), primary_key=True, nullable=False, index=True)

    employee = db.relationship('Employee')
    report_sprint = db.relationship('Report')


class EmployeeRole(db.Model):
    __tablename__ = 'Employee_role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


t_Employee_task = db.Table(
    'Employee_task', db.metadata,
    db.Column('employee_id', db.ForeignKey('Employee.id'), primary_key=True, nullable=False, index=True),
    db.Column('task_id', db.ForeignKey('Task.id'), primary_key=True, nullable=False, index=True)
)


class FreetimeType(db.Model):
    __tablename__ = 'Freetime_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class Project(db.Model):
    __tablename__ = 'Project'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float(asdecimal=True), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False,
                           server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    finish_time = db.Column(db.DateTime)


class ProjectEmployeeRole(db.Model):
    __tablename__ = 'Project_employee_role'

    rate = db.Column(db.Float(asdecimal=True), nullable=False)
    employee_id = db.Column(db.ForeignKey('Employee.id'), primary_key=True, nullable=False, index=True)
    project_id = db.Column(db.ForeignKey('Project.id'), primary_key=True, nullable=False, index=True)
    employee_role_id = db.Column(db.ForeignKey('Employee_role.id'), nullable=False, index=True)

    employee = db.relationship('Employee')
    employee_role = db.relationship('EmployeeRole')
    project = db.relationship('Project')


class Sprint(db.Model):
    __tablename__ = 'Sprint'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    project_id = db.Column(db.ForeignKey('Project.id'), primary_key=True, nullable=False, index=True)
    start_time = db.Column(db.DateTime, nullable=False,
                           server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    finish_time = db.Column(db.DateTime)

    project = db.relationship('Project')


class Report(Sprint):
    __tablename__ = 'Report'

    sprint_id = db.Column(db.ForeignKey('Sprint.id'), primary_key=True, index=True)
    generation_time = db.Column(db.DateTime, nullable=False,
                                server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    description = db.Column(db.Text, nullable=False)


class Stage(db.Model):
    __tablename__ = 'Stage'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class Summarize(db.Model):
    __tablename__ = 'Summarize'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    employee_id = db.Column(db.ForeignKey('Employee.id'), primary_key=True, nullable=False, index=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Float(asdecimal=True), nullable=False)

    employee = db.relationship('Employee')


class Task(db.Model):
    __tablename__ = 'Task'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    stage_id = db.Column(db.ForeignKey('Stage.id'), nullable=False, index=True)
    sprint_id = db.Column(db.ForeignKey('Sprint.id'), primary_key=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False,
                              server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    employee = db.relationship('Employee', secondary='Employee_task')
    sprint = db.relationship('Sprint')
    stage = db.relationship('Stage')


class Worklog(db.Model):
    __tablename__ = 'Worklog'

    employee_id = db.Column(db.ForeignKey('Employee.id'), primary_key=True, nullable=False, index=True)
    task_id = db.Column(db.ForeignKey('Task.id'), primary_key=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    work_date = db.Column(db.Date, nullable=False)
    logged_hours = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.DateTime, primary_key=True, nullable=False,
                              server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    employee = db.relationship('Employee')
    task = db.relationship('Task')
