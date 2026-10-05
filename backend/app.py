from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "project": "CAREERPATH",
        "message": "CAREERPATH Backend is running successfully!",
        "status": "online"
    })


@app.route("/api/status")
def status():
    return jsonify({
        "success": True,
        "message": "Backend API is working",
        "project": "Smart Career Guidance & Opportunity Portal"
    })


@app.route("/api/features")
def features():
    return jsonify({
        "features": [
            "Career Guidance",
            "Career Quiz",
            "Career Recommendation",
            "Skill Gap Analysis",
            "Jobs & Internships",
            "Courses & Skill Development",
            "Resume Builder",
            "Interview Simulator",
            "Job Application Tracker",
            "Career Dashboard",
            "Career Roadmap",
            "AI Career Mentor",
            "Company & Role Explorer"
        ]
    })


if __name__ == "__main__":
    app.run(debug=True)
from flask import Blueprint, request, jsonify
from database import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint("api", __name__, url_prefix="/api")


# =========================================================
# 1. REGISTER
# =========================================================

@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    education = data.get("education", "")
    phone = data.get("phone", "")
    location = data.get("location", "")

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "Name, email and password are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    try:
        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users
            (name, email, password, education, phone, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            email,
            hashed_password,
            education,
            phone,
            location
        ))

        connection.commit()
        user_id = cursor.lastrowid

        return jsonify({
            "success": True,
            "message": "Account created successfully",
            "user_id": user_id
        }), 201

    except Exception:
        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 409

    finally:
        connection.close()


# =========================================================
# 2. LOGIN
# =========================================================

@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    connection.close()

    if user and check_password_hash(user["password"], password):
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "education": user["education"],
                "phone": user["phone"],
                "location": user["location"]
            }
        })

    return jsonify({
        "success": False,
        "message": "Invalid email or password"
    }), 401


# =========================================================
# 3. GET USER PROFILE
# =========================================================

@api.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, email, education, phone, location FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        connection.close()
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    cursor.execute(
        "SELECT skill_name, skill_level FROM skills WHERE user_id = ?",
        (user_id,)
    )

    skills = cursor.fetchall()
    connection.close()

    return jsonify({
        "success": True,
        "profile": dict(user),
        "skills": [dict(skill) for skill in skills]
    })


# =========================================================
# 4. UPDATE PROFILE
# =========================================================

@api.route("/profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):
    data = request.get_json()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE users
        SET name = ?,
            education = ?,
            phone = ?,
            location = ?
        WHERE id = ?
    """, (
        data.get("name"),
        data.get("education"),
        data.get("phone"),
        data.get("location"),
        user_id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Profile updated successfully"
    })


# =========================================================
# 5. GET JOBS
# =========================================================

@api.route("/jobs", methods=["GET"])
def get_jobs():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")

    jobs = cursor.fetchall()
    connection.close()

    return jsonify({
        "success": True,
        "jobs": [dict(job) for job in jobs]
    })


# =========================================================
# 6. GET COURSES
# =========================================================

@api.route("/courses", methods=["GET"])
def get_courses():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM courses ORDER BY id DESC")

    courses = cursor.fetchall()
    connection.close()

    return jsonify({
        "success": True,
        "courses": [dict(course) for course in courses]
    })


# =========================================================
# 7. ADD SKILL
# =========================================================

@api.route("/skills", methods=["POST"])
def add_skill():
    data = request.get_json()

    user_id = data.get("user_id")
    skill_name = data.get("skill_name")
    skill_level = data.get("skill_level", "Beginner")

    if not user_id or not skill_name:
        return jsonify({
            "success": False,
            "message": "User ID and skill name are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO skills
        (user_id, skill_name, skill_level)
        VALUES (?, ?, ?)
    """, (
        user_id,
        skill_name,
        skill_level
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Skill added successfully"
    })


# =========================================================
# 8. SAVE OPPORTUNITY
# =========================================================

@api.route("/saved", methods=["POST"])
def save_opportunity():
    data = request.get_json()

    user_id = data.get("user_id")
    job_id = data.get("job_id")

    if not user_id or not job_id:
        return jsonify({
            "success": False,
            "message": "User ID and Job ID are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id FROM saved_opportunities
        WHERE user_id = ? AND job_id = ?
    """, (user_id, job_id))

    existing = cursor.fetchone()

    if existing:
        connection.close()

        return jsonify({
            "success": False,
            "message": "Opportunity already saved"
        }), 409

    cursor.execute("""
        INSERT INTO saved_opportunities
        (user_id, job_id)
        VALUES (?, ?)
    """, (
        user_id,
        job_id
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Opportunity saved successfully"
    })


# =========================================================
# 9. GET SAVED OPPORTUNITIES
# =========================================================

@api.route("/saved/<int:user_id>", methods=["GET"])
def get_saved_opportunities(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT jobs.*
        FROM jobs
        INNER JOIN saved_opportunities
        ON jobs.id = saved_opportunities.job_id
        WHERE saved_opportunities.user_id = ?
        ORDER BY saved_opportunities.id DESC
    """, (user_id,))

    jobs = cursor.fetchall()
    connection.close()

    return jsonify({
        "success": True,
        "saved_opportunities": [dict(job) for job in jobs]
    })


# =========================================================
# 10. APPLY FOR JOB
# =========================================================

@api.route("/applications", methods=["POST"])
def apply_for_job():
    data = request.get_json()

    user_id = data.get("user_id")
    job_id = data.get("job_id")

    if not user_id or not job_id:
        return jsonify({
            "success": False,
            "message": "User ID and Job ID are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id FROM applications
        WHERE user_id = ? AND job_id = ?
    """, (user_id, job_id))

    existing = cursor.fetchone()

    if existing:
        connection.close()

        return jsonify({
            "success": False,
            "message": "Already applied for this job"
        }), 409

    cursor.execute("""
        INSERT INTO applications
        (user_id, job_id, status)
        VALUES (?, ?, ?)
    """, (
        user_id,
        job_id,
        "Applied"
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Application submitted successfully"
    })


# =========================================================
# 11. APPLICATION TRACKER
# =========================================================

@api.route("/applications/<int:user_id>", methods=["GET"])
def get_applications(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            applications.id,
            applications.status,
            applications.applied_at,
            jobs.title,
            jobs.company,
            jobs.location
        FROM applications
        INNER JOIN jobs
        ON applications.job_id = jobs.id
        WHERE applications.user_id = ?
        ORDER BY applications.id DESC
    """, (user_id,))

    applications = cursor.fetchall()
    connection.close()

    return jsonify({
        "success": True,
        "applications": [dict(application) for application in applications]
    })


# =========================================================
# 12. CAREER QUIZ RESULT
# =========================================================

@api.route("/quiz-result", methods=["POST"])
def save_quiz_result():
    data = request.get_json()

    user_id = data.get("user_id")
    career_result = data.get("career_result")
    score = data.get("score", 0)

    if not user_id or not career_result:
        return jsonify({
            "success": False,
            "message": "User ID and career result are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO quiz_results
        (user_id, career_result, score)
        VALUES (?, ?, ?)
    """, (
        user_id,
        career_result,
        score
    ))

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Career quiz result saved successfully",
        "career": career_result,
        "score": score
    })


# =========================================================
# 13. USER QUIZ HISTORY
# =========================================================

@api.route("/quiz-result/<int:user_id>", methods=["GET"])
def get_quiz_results(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM quiz_results
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    results = cursor.fetchall()
    connection.close()

    return jsonify({
        "success": True,
        "results": [dict(result) for result in results]
    })


# =========================================================
# 14. BACKEND HEALTH CHECK
# =========================================================

@api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "project": "CAREERPATH",
        "backend": "online",
        "message": "CAREERPATH API is working successfully"
    })
from flask import Flask, jsonify

from database import create_database
from routes import api
from admin_routes import admin_api
from recommendation import recommendation_api
from application_routes import application_api


# =========================================================
# CAREERPATH BACKEND APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# CREATE DATABASE
# =========================================================

create_database()


# =========================================================
# REGISTER API BLUEPRINTS
# =========================================================

# Main APIs
app.register_blueprint(api)

# Admin Management APIs
app.register_blueprint(admin_api)

# Career Recommendation APIs
app.register_blueprint(recommendation_api)

# Application Management APIs
app.register_blueprint(application_api)


# =========================================================
# HOME / BACKEND STATUS
# =========================================================

@app.route("/")
def home():

    return jsonify({
        "project": "CAREERPATH",
        "status": "Backend is running",
        "message": "Smart Career Guidance & Opportunity Portal",
        "version": "1.0.0"
    })


# =========================================================
# FEATURES API
# =========================================================

@app.route("/api/features")
def features():

    return jsonify({

        "success": True,

        "project": "CAREERPATH",

        "features": [

            "Career Guidance",
            "Career Quiz",
            "Career Recommendation",
            "Skill Gap Analysis",

            "Jobs & Internships",
            "Courses & Skill Development",

            "Save Opportunities",
            "Application Tracking",

            "Resume Builder",
            "Resume Job Match",

            "Interview Simulator",
            "Interview Question Bank",

            "Career Roadmap",
            "Career Action Plan",

            "Career Readiness Score",
            "Career Progress Tracker",

            "AI Career Mentor",
            "AI Resume Analyzer",

            "Career Simulation Lab",
            "Career Comparison",

            "Company & Role Explorer",

            "Admin Dashboard"
        ]
    })


# =========================================================
# API INFORMATION
# =========================================================

@app.route("/api")
def api_information():

    return jsonify({

        "project": "CAREERPATH",

        "message": "CAREERPATH API is working successfully",

        "modules": {

            "main_api": "/api",

            "admin": "/api/admin",

            "recommendation": "/api/recommendation",

            "application": "/api/application"
        },

        "available_health_checks": [

            "/api/health",

            "/api/admin/health",

            "/api/recommendation/health",

            "/api/application/health"
        ]
    })


# =========================================================
# BACKEND HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({

        "success": True,

        "project": "CAREERPATH",

        "backend": "online",

        "status": "healthy",

        "message": "CAREERPATH backend is working successfully"
    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
