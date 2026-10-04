from flask import Blueprint, request, jsonify
from database import get_connection

recommendation_api = Blueprint(
    "recommendation_api",
    __name__,
    url_prefix="/api/recommendation"
)


# ---------------------------------------------------------
# Career Recommendation Engine
# ---------------------------------------------------------

def calculate_recommendations(skills, interests):
    recommendations = []

    skills_text = " ".join(skills).lower()
    interests_text = " ".join(interests).lower()

    text = skills_text + " " + interests_text

    career_rules = [
        {
            "career": "Software Developer",
            "keywords": [
                "python",
                "java",
                "programming",
                "coding",
                "software",
                "problem solving"
            ],
            "description": "Build software applications and solve programming problems.",
            "skills": ["Python", "Java", "SQL", "Git"],
            "score": 0
        },
        {
            "career": "Web Developer",
            "keywords": [
                "html",
                "css",
                "javascript",
                "web",
                "website",
                "frontend"
            ],
            "description": "Create responsive and interactive websites.",
            "skills": ["HTML", "CSS", "JavaScript", "React"],
            "score": 0
        },
        {
            "career": "Data Analyst",
            "keywords": [
                "data",
                "sql",
                "excel",
                "analytics",
                "analysis",
                "statistics"
            ],
            "description": "Analyze data and create useful business insights.",
            "skills": ["SQL", "Excel", "Python", "Power BI"],
            "score": 0
        },
        {
            "career": "AI / Machine Learning Engineer",
            "keywords": [
                "ai",
                "machine learning",
                "artificial intelligence",
                "python",
                "data science",
                "ml"
            ],
            "description": "Develop intelligent systems using AI and machine learning.",
            "skills": ["Python", "Machine Learning", "Statistics", "Data Science"],
            "score": 0
        },
        {
            "career": "UI/UX Designer",
            "keywords": [
                "design",
                "ui",
                "ux",
                "creative",
                "figma",
                "user experience"
            ],
            "description": "Design attractive and user-friendly digital experiences.",
            "skills": ["Figma", "UI Design", "UX Research", "Prototyping"],
            "score": 0
        },
        {
            "career": "Cyber Security Analyst",
            "keywords": [
                "security",
                "cyber",
                "networking",
                "linux",
                "ethical hacking",
                "cyber security"
            ],
            "description": "Protect systems, networks and applications from security threats.",
            "skills": ["Networking", "Linux", "Cyber Security", "Ethical Hacking"],
            "score": 0
        },
        {
            "career": "Cloud Engineer",
            "keywords": [
                "cloud",
                "aws",
                "azure",
                "server",
                "devops",
                "deployment"
            ],
            "description": "Manage cloud infrastructure and modern application deployment.",
            "skills": ["AWS", "Azure", "Linux", "DevOps"],
            "score": 0
        }
    ]

    for career in career_rules:
        for keyword in career["keywords"]:
            if keyword in text:
                career["score"] += 1

    career_rules.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    for career in career_rules:
        if career["score"] > 0:
            recommendations.append({
                "career": career["career"],
                "match_score": min(
                    career["score"] * 15,
                    100
                ),
                "description": career["description"],
                "recommended_skills": career["skills"]
            })

    # Default recommendations if no matching keyword is found
    if not recommendations:
        recommendations = [
            {
                "career": "Software Developer",
                "match_score": 50,
                "description": "A good starting career for students interested in technology and programming.",
                "recommended_skills": [
                    "Python",
                    "Java",
                    "SQL",
                    "Git"
                ]
            },
            {
                "career": "Web Developer",
                "match_score": 45,
                "description": "A suitable option for students interested in websites and frontend development.",
                "recommended_skills": [
                    "HTML",
                    "CSS",
                    "JavaScript",
                    "React"
                ]
            }
        ]

    return recommendations[:5]


# ---------------------------------------------------------
# Generate Recommendations
# ---------------------------------------------------------

@recommendation_api.route("/", methods=["POST"])
def recommend_career():

    data = request.get_json() or {}

    skills = data.get("skills", [])
    interests = data.get("interests", [])

    if isinstance(skills, str):
        skills = [skills]

    if isinstance(interests, str):
        interests = [interests]

    recommendations = calculate_recommendations(
        skills,
        interests
    )

    return jsonify({
        "success": True,
        "message": "Career recommendations generated successfully",
        "recommendations": recommendations
    })


# ---------------------------------------------------------
# Recommendation Based on User Profile
# ---------------------------------------------------------

@recommendation_api.route(
    "/user/<int:user_id>",
    methods=["GET"]
)
def recommend_for_user(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    # Check user
    cursor.execute(
        """
        SELECT id, name, education
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        connection.close()

        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    # Get user skills
    cursor.execute(
        """
        SELECT skill_name, skill_level
        FROM skills
        WHERE user_id = ?
        """,
        (user_id,)
    )

    skill_rows = cursor.fetchall()

    connection.close()

    skills = [
        skill["skill_name"]
        for skill in skill_rows
    ]

    interests = []

    recommendations = calculate_recommendations(
        skills,
        interests
    )

    return jsonify({
        "success": True,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "education": user["education"]
        },
        "skills": skills,
        "recommendations": recommendations
    })


# ---------------------------------------------------------
# Career Categories
# ---------------------------------------------------------

@recommendation_api.route(
    "/careers",
    methods=["GET"]
)
def career_categories():

    careers = [
        "Software Developer",
        "Web Developer",
        "Data Analyst",
        "AI / Machine Learning Engineer",
        "UI/UX Designer",
        "Cyber Security Analyst",
        "Cloud Engineer"
    ]

    return jsonify({
        "success": True,
        "careers": careers
    })


# ---------------------------------------------------------
# Recommendation API Health Check
# ---------------------------------------------------------

@recommendation_api.route(
    "/health",
    methods=["GET"]
)
def recommendation_health():

    return jsonify({
        "success": True,
        "module": "Career Recommendation Engine",
        "status": "online",
        "message": "Career recommendation API is working"
    })


if __name__ == "__main__":
    print(
        "CAREERPATH Career Recommendation Engine loaded successfully!"
    )
