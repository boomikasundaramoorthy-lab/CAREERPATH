# =========================================================
# CAREERPATH - AUTHENTICATION HELPER
# =========================================================

from functools import wraps

from flask import request, jsonify

from database import get_connection


# =========================================================
# GET USER FROM REQUEST
# =========================================================

def get_current_user():

    user_id = request.headers.get("X-User-ID")

    if not user_id:
        return None

    try:
        user_id = int(user_id)
    except ValueError:
        return None

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            education,
            phone,
            location
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    return user


# =========================================================
# REQUIRE LOGIN
# =========================================================

def login_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        user = get_current_user()

        if not user:

            return jsonify({
                "success": False,
                "message": "Please login to continue"
            }), 401

        return function(
            *args,
            **kwargs
        )

    return decorated_function


# =========================================================
# CHECK USER EXISTS
# =========================================================

def user_exists(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    return user is not None


# =========================================================
# GET USER ID
# =========================================================

def get_user_id():

    user_id = request.headers.get("X-User-ID")

    if not user_id:
        return None

    try:
        return int(user_id)
    except ValueError:
        return None


# =========================================================
# AUTHENTICATION STATUS
# =========================================================

def authentication_status():

    user = get_current_user()

    if user:

        return {
            "logged_in": True,
            "user": dict(user)
        }

    return {
        "logged_in": False,
        "user": None
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print(
        "CAREERPATH authentication helper loaded successfully!"
    )
