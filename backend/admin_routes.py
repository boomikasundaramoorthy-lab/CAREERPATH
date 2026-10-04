from flask import Blueprint, jsonify, request
from database import get_connection

admin_api = Blueprint(
    "admin_api",
    __name__,
    url_prefix="/api/admin"
)


# =========================================================
# 1. ADMIN DASHBOARD STATISTICS
# =========================================================

@admin_api.route("/stats", methods=["GET"])
def admin_stats():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM users")
    students = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM jobs")
    jobs = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM courses")
    courses = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM applications")
    applications = cursor.fetchone()["total"]

    connection.close()

    return jsonify({
        "success": True,
        "stats": {
            "students": students,
            "jobs": jobs,
            "courses": courses,
            "applications": applications
        }
    })


# =========================================================
# 2. GET ALL STUDENTS
# =========================================================

@admin_api.route("/students", methods=["GET"])
def get_students():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            education,
            phone,
            location,
            created_at
        FROM users
        ORDER BY id DESC
    """)

    students = cursor.fetchall()

    connection.close()

    return jsonify({
        "success": True,
        "students": [
            dict(student)
            for student in students
        ]
    })


# =========================================================
# 3. GET ALL JOBS
# =========================================================

@admin_api.route("/jobs", methods=["GET"])
def admin_jobs():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM jobs
        ORDER BY id DESC
    """)

    jobs = cursor.fetchall()

    connection.close()

    return jsonify({
        "success": True,
        "jobs": [
            dict(job)
            for job in jobs
        ]
    })


# =========================================================
# 4. ADD NEW JOB
# =========================================================

@admin_api.route("/jobs", methods=["POST"])
def add_job():

    data = request.get_json()

    title = data.get("title")
    company = data.get("company")
    location = data.get("location")
    job_type = data.get("job_type")
    description = data.get("description")
    skills = data.get("skills")

    if not title:

        return jsonify({
            "success": False,
            "message": "Job title is required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO jobs
        (
            title,
            company,
            location,
            job_type,
            description,
            skills
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        company,
        location,
        job_type,
        description,
        skills
    ))

    connection.commit()

    job_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "success": True,
        "message": "Job added successfully",
        "job_id": job_id
    }), 201


# =========================================================
# 5. DELETE JOB
# =========================================================

@admin_api.route("/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM jobs WHERE id = ?",
        (job_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    if deleted == 0:

        return jsonify({
            "success": False,
            "message": "Job not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Job deleted successfully"
    })


# =========================================================
# 6. GET ALL COURSES
# =========================================================

@admin_api.route("/courses", methods=["GET"])
def admin_courses():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM courses
        ORDER BY id DESC
    """)

    courses = cursor.fetchall()

    connection.close()

    return jsonify({
        "success": True,
        "courses": [
            dict(course)
            for course in courses
        ]
    })


# =========================================================
# 7. ADD NEW COURSE
# =========================================================

@admin_api.route("/courses", methods=["POST"])
def add_course():

    data = request.get_json()

    title = data.get("title")
    category = data.get("category")
    level = data.get("level")
    duration = data.get("duration")
    description = data.get("description")

    if not title:

        return jsonify({
            "success": False,
            "message": "Course title is required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO courses
        (
            title,
            category,
            level,
            duration,
            description
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        category,
        level,
        duration,
        description
    ))

    connection.commit()

    course_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "success": True,
        "message": "Course added successfully",
        "course_id": course_id
    }), 201


# =========================================================
# 8. DELETE COURSE
# =========================================================

@admin_api.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM courses WHERE id = ?",
        (course_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    if deleted == 0:

        return jsonify({
            "success": False,
            "message": "Course not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Course deleted successfully"
    })


# =========================================================
# 9. RECENT APPLICATIONS
# =========================================================

@admin_api.route("/applications", methods=["GET"])
def admin_applications():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            applications.id,
            applications.status,
            applications.applied_at,
            users.name,
            users.email,
            jobs.title,
            jobs.company
        FROM applications
        INNER JOIN users
            ON applications.user_id = users.id
        INNER JOIN jobs
            ON applications.job_id = jobs.id
        ORDER BY applications.id DESC
    """)

    applications = cursor.fetchall()

    connection.close()

    return jsonify({
        "success": True,
        "applications": [
            dict(application)
            for application in applications
        ]
    })


# =========================================================
# 10. ADMIN HEALTH CHECK
# =========================================================

@admin_api.route("/health", methods=["GET"])
def admin_health():

    return jsonify({
        "success": True,
        "module": "Admin Management",
        "status": "online",
        "message": "CAREERPATH Admin API is working"
    })
