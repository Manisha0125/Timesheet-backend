from flask import Flask
from databasefile import init_db

app = Flask(__name__)
# @app.route('/')
# def base_route():
#     return "Hello... We Are Online."
from  application_routes import *


# init_db(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timesheet.db'  # Or use PostgreSQL/MySQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# timesheet = [
#     {
#         "timesheet_id": 203,
#         "employee_id": 102,
#         "week_start_date": "2025-02-10",
#         "week_end_date": "2025-02-14",
#         "task_name": "API Development",
#         "total_hours": 38,
#         "status": "Pending",
#         "entries": [
#             {
#                 "timesheet_id": 203,
#                 "day": "Monday",
#                 "date": "2025-02-10",
#                 "project_name": "Timesheet System",
#                 "types": "working",
#                 "working_hour": 8,
#                 "time_slot": [
#                     {"first_slot": "API Design", "second_slot": "Database Setup"}
#                 ],
#                 "project_id": 301,
#                 "description": "Designed API structure and connected database",
#                 "links": ["https://github.com/Manisha0125/Timesheet-Backend"],
#                 "category": "Development"
#             },
#             {
#                 "timesheet_id": 203,
#                 "day": "Tuesday",
#                 "date": "2025-02-11",
#                 "project_name": "Timesheet System",
#                 "types": "working",
#                 "working_hour": 7,
#                 "time_slot": [
#                     {"first_slot": "Authentication Module", "second_slot": "Testing"}
#                 ],
#                 "project_id": 301,
#                 "description": "Implemented user authentication and conducted unit tests",
#                 "links": ["https://github.com/Manisha0125/Timesheet-Backend"],
#                 "category": "Development"
#             }
#         ]
#     }
# ]

# @app.route('/timesheet', methods=['GET http://127.0.0.1:5000/timesheet'])
# def get_timesheet():
#  return jsonify(timesheet)

# url = "http://127.0.0.1:5000/timesheetslot_entries"
# data = {
#     "timesheet_id": 1,
#     "project_name": "AI Model Training",
#     "project_id": 202,
#     "description": "Worked on model accuracy improvements",
#     "links": "https://example.com/report",
#     "category": "AI Research",
#     "day_entry": 1
# }

# response = requests.post(url, json=data)
# print(response.json())  # Expected Output: {"message": "Timesheet slot entry created", "id": 1}

init_db(app)     

from Model import *

if __name__ == "__main__":
    # print("Test debug")
    db.create_all()
    app.run(debug=True,host='0.0.0.0')
    # with app.app_context():
    #     db.create_all()  # Create all tables
    # print("Database created successfully!")


