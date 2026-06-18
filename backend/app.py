from flask import Flask, jsonify, request
from flask_cors import CORS

import db
import re
app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    
    students = db.get_all_students()
    if not students:
        return None, 400
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    student_data = request.json
    if not re.match("[A-Z]{4}[0-9]{4}", student_data["course"]):
        return jsonify({"error": "Invalid Course Name"}), 400
    if "mark" not in student_data:
        student = db.insert_student(student_data["name"], student_data["course"], 0)
    else:
        student = db.insert_student(student_data["name"], student_data["course"], student_data["mark"])
    if student:
        return student, 200
    return jsonify({"error": "Failed to add student"}), 400

def checkRequest(student_data):
    if not student_data:
        return False
    elif "name" not in student_data or "course" not in student_data or "mark" not in student_data:
        return False
    elif not isinstance(student_data["mark"], int):
        return False
    elif student_data["mark"] < 0 or student_data["mark"] >  100:
        print("mark")
        return False
    elif not re.match("[A-Z]{4}[0-9]{4}", student_data["course"]):
        print("course")
        return False
    else:
        return True

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json
    if not re.match("[A-Z]{4}[0-9]{4}", student_data["course"]):
        return jsonify({"error": "Invalid Course Name"}), 400
    student = db.update_student(student_id, student_data["name"], student_data["course"], student_data["mark"])
    if not student:
        return jsonify({"error": "Can't find student"}), 404
    return student, 200

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    student = db.get_student_by_id(student_id)
    if not db.delete_student(student_id):
        return jsonify({'error': 'Cant find student'}), 404
    return student, 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = []
    for student in students:
        marks.append(student['mark'])
    count = len(marks)
    if count != 0:
        average = sum(marks) / count
        minimum = min(marks)
        maximum = max(marks)
    else:
        average = 0
        minimum = 0
        maximum = 0
    return jsonify({'count': count, 
                    "average": average, 
                    "min": minimum,
                    "max": maximum})


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
