from datetime import datetime
from flask import  request, jsonify
from databasefile import db
from Model import DayEntry, Employee, TimesheetComment, TimesheetslotEntry, WeekEntry
from app import app



@app.route("/")
def home():
    return "Hello"


# Create a new employee entry
@app.route('/employees', methods=['POST'])
def create_employee():
 try:  
    data = request.json    
    new_employee = Employee(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        role=data['role'],
        manager_id=data.get('manager_id'),
        # created_at=data['created_at'],
        # updated_at = data['updated_at'],
        department = data['department']
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify({"message": "Employee created successfully"}), 201
 except Exception as ex:
    print(ex)

url = "http://127.0.0.1:5000/employees"

@app.route('/employees', methods=['GET'])
def get_employees():
    employees = []
    try:
       
        employees = Employee.query.all()
        print(employees)
    except Exception as error:
        print(error)
    return jsonify(employees)



# Create a new weekentry 
@app.route('/week_entries', methods=['POST'])
def create_week_entry():
 try:
    data = request.json
    week_start_date = datetime.strptime(data['week_start_date'], '%d-%m-%Y')
    week_end_date = datetime.strptime(data['week_end_date'], '%d-%m-%Y',)

    new_entry = WeekEntry(
        employee_id=data['employee_id'],
        week_start_date=datetime.strptime(data['week_start_date'], '%d-%m-%Y'), # Expecting a string in 'DD-MM-YYYY'format
        week_end_date=datetime.strptime(data['week_end_date'], '%d-%m-%Y'),  # Expecting a string in 'DD-MM-YYYY' format
        task_name=data['task_name'],
        total_hours=data['total_hours'],
        status=data['status']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Week entry created", "timesheet_id": new_entry.timesheet_id}), 201
 except Exception as ex:
        return {"error":str(ex)}

url = "http://127.0.0.1:5000/week_entries"

@app.route('/week_entries', methods=['GET'])
def get_week_entries():
    entries = WeekEntry.query.all()
    return jsonify([
        {
            "timesheet_id": entry.timesheet_id,
            "employee_id": entry.employee_id,
            "week_start_date": entry.week_start_date.strftime("%d-%m-%y"),
            "week_end_date": entry.week_end_date.strftime("%d-%m-%y"),
            "task_name": entry.task_name,
            "total_hours": entry.total_hours,
            "status": entry.status
        } for entry in entries
    ])

# Create a New dayEntry

url = "http://127.0.0.1:5000/day_entries"

@app.route('/day_entries', methods=['GET'])
def get_day_entries():
    entries = DayEntry.query.all()
    return jsonify([
        {
            "id": entry.id,
            "timesheet_id": entry.timesheet_id,
            "date": entry.date.strftime("%Y-%m-%d"),
            "employee_id": entry.employee_id,
            "project_name": entry.project_name,
            "types": entry.types,
            "working_hour": entry.working_hour,
            "time_slot": entry.time_slot
        } for entry in entries
    ])

@app.route('/day_entries', methods=['POST'])
def create_day_entry():
    try:
        data = request.json
        valid_types = ["Working", "Holiday", "Leave"]
        
        if data['types'] not in valid_types:
            return jsonify({"error": "Invalid type. Allowed values: Working, Holiday, Leave"}), 400
        
        formatted_date = datetime.strptime(data['date'], "%d-%m-%Y").date()
        new_entry = DayEntry(
            timesheet_id=data['timesheet_id'],
            date=formatted_date,
            employee_id=data['employee_id'],
            types=data['types'],
            working_hour=data['working_hour']
        )
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Day entry created", "id": new_entry.id}), 201
    except Exception as ex:
        return {"error": str(ex)}

#  Create a New timeslotentry

url = "http://127.0.0.1:5000/timesheetslot_entries"

@app.route('/timesheetslot_entries', methods=['GET'])
def get_timesheetslot_entries():
    entries = TimesheetslotEntry.query.all()
    return jsonify([
        {
            "id": entry.id,
            "timesheet_id": entry.timesheet_id,
            "project_name": entry.project_name,
            "project_id": entry.project_id,
            "description": entry.description,
            "links": entry.links,
            "category": entry.category,
            "day_entry": entry.day_entry
        } for entry in entries
    ])

@app.route('/timesheetslot_entries', methods=['POST'])
def create_timesheetslot_entry():
    try:
        data = request.json

        # Ensure category is properly formatted
        if isinstance(data['category'], list):  
            categories = ",".join(data['category'])  # Convert list to comma-separated string
        elif isinstance(data['category'], str):  
            categories = data['category']  # Use as-is if already a string
        else:
            return jsonify({"error": "Invalid category format"}), 400

        # Convert date and time to datetime format
        day_entry = datetime.strptime(data['day_entry'], '%d-%m-%Y').date()
        time_start_slot = datetime.strptime(f"{data['day_entry']} {data['time_start_slot']}", "%d-%m-%Y %H:%M:%S")
        time_end_slot = datetime.strptime(f"{data['day_entry']} {data['time_end_slot']}", "%d-%m-%Y %H:%M:%S")

        # Create new entry
        new_entry = TimesheetslotEntry(
            timesheet_id=data['timesheet_id'],
            day_entry=day_entry,
            time_start_slot=time_start_slot,
            time_end_slot=time_end_slot,
            project_name=data['project_name'],
            project_id=data['project_id'],
            description=data.get('description'),
            links=data.get('links'),
            category=categories  # Store as a comma-separated string
        )

        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Timesheet slot entry created", "id": new_entry.id}), 201

    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


# create a  New timesheetcomment

@app.route('/timesheet_comments', methods=['POST'])
def create_timesheet_comment():
    data = request.json
    new_comment = TimesheetComment(
        timesheet_id=data['timesheet_id'],
        comment_text=data['comment_text'],
        comment_by=data['comment_by'],
        created_by=data['created_by']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Timesheet comment created", "comment_id": new_comment.comment_id}), 201

url = "http://127.0.0.1:5000/timesheet_comments"

@app.route('/timesheet_comments', methods=['GET'])
def get_timesheet_comments():
    comments = TimesheetComment.query.all()
    return jsonify([
        {
            "comment_id": comment.comment_id,
            "timesheet_id": comment.timesheet_id,
            "comment_text": comment.comment_text,
            "comment_by": comment.comment_by,
            "created_by": comment.created_by
        } for comment in comments
    ])