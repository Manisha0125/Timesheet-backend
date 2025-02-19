from databasefile import db
from sqlalchemy import Enum 

class Employee(db.Model):
    __tablename__ = 'employees'

    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=True)
    role = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=True)
    # created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    # updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    department = db.Column(db.String(100), nullable=True)

    # Relationship to Self for manager-Employee hierarchy
    # manager = db.relationship("Employee", remote_side=[employee_id], backref="team_members")

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name}>"


class WeekEntry(db.Model):
    __tablename__ = 'weekentry'

    timesheet_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    week_start_date = db.Column(db.Date, nullable=False)
    week_end_date = db.Column(db.Date, nullable=False)
    task_name = db.Column(db.String(255), nullable=False)
    total_hours = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)

    # Relationship to Employee
    # employee = db.relationship("Employee", backref="timesheets")

    def __repr__(self):
        return f"<WeekEntry {self.employee_id} - {self.week_start_date}>"


class DayEntry(db.Model):
    __tablename__ = 'day_entries'

    types_enum = ("Working", "Holiday", "Leave")
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timesheet_id = db.Column(db.Integer, db.ForeignKey('weekentry.timesheet_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    types = db.Column(Enum(*types_enum, name="entry_types"), nullable=False)
    working_hour = db.Column(db.Float, nullable=False)

    

    # Relationships
    # timesheet = db.relationship("WeekEntry", backref="day_entries")
    # employee = db.relationship("Employee", backref="day_entries")

    def __repr__(self):
        return f"<DayEntry {self.project_name} - {self.types}>"

class TimesheetslotEntry(db.Model):
    __tablename__ = 'timesheet_entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timesheet_id = db.Column(db.Integer, db.ForeignKey('weekentry.timesheet_id'), nullable=False)
    day_entry = db.Column(db.String(20), nullable=False)
    time_start_slot = db.Column(db.String, nullable=False)
    time_end_slot = db.Column(db.String, nullable=False)
    project_name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    links = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<TimesheetslotEntry {self.project_name} - {self.time_period} - {self.time_slot} hours>"

    # Relationships
    # timesheet = db.relationship("WeekEntry", backref="timesheet_entries")
    # employee = db.relationship("Employee", backref="timesheet_entries")

    def __repr__(self):
        return f"<TimesheetslotEntry {self.project_name} - {self.links}>"

class TimesheetComment(db.Model):
    __tablename__ = 'timesheet_comments'

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timesheet_id = db.Column(db.Integer, db.ForeignKey('weekentry.timesheet_id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    comment_by = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.String(100), nullable=False)

    # Relationship
    # timesheet = db.relationship("WeekEntry", backref="comments")

    def __repr__(self):
        return f"<TimesheetComment {self.comment_text} - {self.comment_by}>"
