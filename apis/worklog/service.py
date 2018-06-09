from my_app import db
from database.models import Worklog
from database.schemas import WorklogSchema


def log_work(worklog_json):
    worklog = WorklogSchema().load(worklog_json).data

    db.session.add(worklog)
    db.session.flush()
    if worklog in db.session:
        db.session.commit()
        return WorklogSchema().jsonify(worklog)
    else:
        db.session.rollback()
        return {'error': 'Work is not logged'}, 503
