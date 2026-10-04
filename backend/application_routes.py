from flask import Blueprint, request, jsonify
from database import get_connection

application_api = Blueprint(
    "application_api",
    __name__,
    url_prefix="/api/application"
)


# =========================================================
# APPLY FOR A JOB
# =========================================================

@application_api.route("/apply", methods=["POST"])
def apply_for_job():

    data = request.get_json() or {}

    user_id = data.get("user_id")
    job_id = data.get("job_id")

    if not user_id or not job_id:
        return jsonify({
            "success": False,
            "message": "User ID and Job ID are required"
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    # Check user
    cursor.execute(
        "SELECT id FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        connection.close()

        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    # Check job
    cursor.execute(
        "SELECT id, title, company FROM jobs WHERE id = ?",
        (job_id,)
    )

    job = cursor.fetchone()

    if not job:
        connection.close()

        return jsonify({
            "success": False,
            "message": "Job not found"
        }), 404

    # Check duplicate application
    cursor.execute(
        """
        SELECT id
        FROM applications
        WHERE user_id = ? AND job_id = ?
        """,
        (user_id, job_id)
    )

    existing = cursor.fetchone()

    if existing:
        connection.close()

        return jsonify({
            "success": False,
            "message": "Already applied for this job"
        }), 409

    # Create application
    cursor.execute(
        """
        INSERT INTO applications
        (user_id, job_id, status)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            job_id,
            "Applied"
        )
    )

    connection.commit()

    application_id = cursor.lastrowid

    connection.close()

    return jsonify({
        "success": True,
        "message": "Application submitted successfully",
        "application_id": application_id,
        "status": "Applied"
    }), 201


# =========================================================
# GET USER APPLICATIONS
# =========================================================

@application_api.route(
    "/user/<int:user_id>",
    methods=["GET"]
)
def get_user_applications(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            applications.id,
            applications.status,
            applications.applied_at,
            jobs.id AS job_id,
            jobs.title,
            jobs.company,
            jobs.location,
            jobs.job_type
        FROM applications
        INNER JOIN jobs
            ON applications.job_id = jobs.id
        WHERE applications.user_id = ?
        ORDER BY applications.id DESC
        """,
        (user_id,)
    )

    applications = cursor.fetchall()

    connection.close()

    return jsonify({
        "success": True,
        "count": len(applications),
        "applications": [
            dict(application)
            for application in applications
        ]
    })


# =========================================================
# GET SINGLE APPLICATION
# =========================================================

@application_api.route(
    "/<int:application_id>",
    methods=["GET"]
)
def get_application(application_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            applications.id,
            applications.status,
            applications.applied_at,
            users.name,
            users.email,
            jobs.title,
            jobs.company,
            jobs.location,
            jobs.job_type
        FROM applications
        INNER JOIN users
            ON applications.user_id = users.id
        INNER JOIN jobs
            ON applications.job_id = jobs.id
        WHERE applications.id = ?
        """,
        (application_id,)
    )

    application = cursor.fetchone()

    connection.close()

    if not application:
        return jsonify({
            "success": False,
            "message": "Application not found"
        }), 404

    return jsonify({
        "success": True,
        "application": dict(application)
    })


# =========================================================
# UPDATE APPLICATION STATUS
# =========================================================

@application_api.route(
    "/<int:application_id>/status",
    methods=["PUT"]
)
def update_application_status(application_id):

    data = request.get_json() or {}

    status = data.get("status")

    allowed_statuses = [
        "Applied",
        "Under Review",
        "Shortlisted",
        "Interview",
        "Selected",
        "Rejected"
    ]

    if not status:
        return jsonify({
            "success": False,
            "message": "Application status is required"
        }), 400

    if status not in allowed_statuses:
        return jsonify({
            "success": False,
            "message": "Invalid application status",
            "allowed_statuses": allowed_statuses
        }), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM applications
        WHERE id = ?
        """,
        (application_id,)
    )

    application = cursor.fetchone()

    if not application:
        connection.close()

        return jsonify({
            "success": False,
            "message": "Application not found"
        }), 404

    cursor.execute(
        """
        UPDATE applications
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            application_id
        )
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Application status updated successfully",
        "application_id": application_id,
        "status": status
    })


# =========================================================
# DELETE / WITHDRAW APPLICATION
# =========================================================

@application_api.route(
    "/<int:application_id>",
    methods=["DELETE"]
)
def withdraw_application(application_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM applications
        WHERE id = ?
        """,
        (application_id,)
    )

    application = cursor.fetchone()

    if not application:
        connection.close()

        return jsonify({
            "success": False,
            "message": "Application not found"
        }), 404

    cursor.execute(
        """
        DELETE FROM applications
        WHERE id = ?
        """,
        (application_id,)
    )

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Application withdrawn successfully"
    })


# =========================================================
# APPLICATION STATISTICS
# =========================================================

@application_api.route(
    "/stats/<int:user_id>",
    methods=["GET"]
)
def application_stats(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total
        FROM applications
        WHERE user_id = ?
        """,
        (user_id,)
    )

    total = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM applications
        WHERE user_id = ?
        AND status = 'Applied'
        """,
        (user_id,)
    )

    applied = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM applications
        WHERE user_id = ?
        AND status = 'Under Review'
        """,
        (user_id,)
    )

    under_review = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM applications
        WHERE user_id = ?
        AND status = 'Shortlisted'
        """,
        (user_id,)
    )

    shortlisted = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM applications
        WHERE user_id = ?
        AND status = 'Interview'
        """,
        (user_id,)
    )

    interview = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM applications
        WHERE user_id = ?
        AND status = 'Selected'
        """,
        (user_id,)
    )

    selected = cursor.fetchone()["count"]

    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM applications
        WHERE user_id = ?
        AND status = 'Rejected'
        """,
        (user_id,)
    )

    rejected = cursor.fetchone()["count"]

    connection.close()

    return jsonify({
        "success": True,
        "statistics": {
            "total": total,
            "applied": applied,
            "under_review": under_review,
            "shortlisted": shortlisted,
            "interview": interview,
            "selected": selected,
            "rejected": rejected
        }
    })


# =========================================================
# APPLICATION API HEALTH CHECK
# =========================================================

@application_api.route(
    "/health",
    methods=["GET"]
)
def application_health():

    return jsonify({
        "success": True,
        "module": "Application Management",
        "status": "online",
        "message": "CAREERPATH Application API is working"
    })


if __name__ == "__main__":

    print(
        "CAREERPATH Application Management API loaded successfully!"
    )
