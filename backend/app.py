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
