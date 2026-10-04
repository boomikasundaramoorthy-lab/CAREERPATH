# =========================================================
# CAREERPATH BACKEND CONFIGURATION
# =========================================================

import os


# =========================================================
# PROJECT INFORMATION
# =========================================================

PROJECT_NAME = "CAREERPATH"

PROJECT_DESCRIPTION = (
    "Smart Career Guidance & Opportunity Portal"
)

VERSION = "1.0.0"


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DATABASE_NAME = "careerpath.db"

DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    DATABASE_NAME
)


# =========================================================
# API CONFIGURATION
# =========================================================

API_PREFIX = "/api"

API_VERSION = "v1"


# =========================================================
# APPLICATION SETTINGS
# =========================================================

DEBUG_MODE = True

HOST = "0.0.0.0"

PORT = 5000


# =========================================================
# CAREERPATH FEATURES
# =========================================================

FEATURES = [

    "Career Guidance",

    "Career Quiz",

    "Career Recommendation",

    "Skill Gap Analysis",

    "Jobs & Internships",

    "Courses & Skill Development",

    "Resume Builder",

    "Resume Job Match",

    "Interview Simulator",

    "Application Tracker",

    "Career Dashboard",

    "Career Roadmap",

    "AI Career Mentor",

    "AI Resume Analyzer",

    "Career Readiness Score",

    "Company & Role Explorer"

]


# =========================================================
# DEFAULT APPLICATION STATUS
# =========================================================

APPLICATION_STATUSES = [

    "Applied",

    "Under Review",

    "Shortlisted",

    "Interview",

    "Selected",

    "Rejected"

]


# =========================================================
# DEFAULT SKILL LEVELS
# =========================================================

SKILL_LEVELS = [

    "Beginner",

    "Intermediate",

    "Advanced",

    "Expert"

]


# =========================================================
# DEFAULT JOB TYPES
# =========================================================

JOB_TYPES = [

    "Full Time",

    "Part Time",

    "Internship",

    "Remote",

    "Hybrid"

]


# =========================================================
# DEFAULT EDUCATION OPTIONS
# =========================================================

EDUCATION_OPTIONS = [

    "BCA",

    "B.Sc",

    "B.Com",

    "B.E / B.Tech",

    "B.A",

    "MCA",

    "M.Sc",

    "MBA",

    "Other"

]


# =========================================================
# CAREER CATEGORIES
# =========================================================

CAREER_CATEGORIES = [

    "Software Development",

    "Web Development",

    "Data Science",

    "Artificial Intelligence",

    "Machine Learning",

    "UI/UX Design",

    "Cyber Security",

    "Cloud Computing",

    "Digital Marketing",

    "Business Analytics"

]


# =========================================================
# CONFIGURATION SUMMARY
# =========================================================

def get_config():

    return {

        "project": PROJECT_NAME,

        "description": PROJECT_DESCRIPTION,

        "version": VERSION,

        "database": DATABASE_NAME,

        "api_prefix": API_PREFIX,

        "debug": DEBUG_MODE,

        "host": HOST,

        "port": PORT,

        "features": FEATURES,

        "application_statuses":
            APPLICATION_STATUSES,

        "skill_levels":
            SKILL_LEVELS,

        "job_types":
            JOB_TYPES,

        "education_options":
            EDUCATION_OPTIONS,

        "career_categories":
            CAREER_CATEGORIES

    }


# =========================================================
# TEST CONFIGURATION
# =========================================================

if __name__ == "__main__":

    print("========================================")

    print("      CAREERPATH BACKEND CONFIG")

    print("========================================")

    print()

    print("Project:", PROJECT_NAME)

    print("Version:", VERSION)

    print("Database:", DATABASE_NAME)

    print("API Prefix:", API_PREFIX)

    print("Host:", HOST)

    print("Port:", PORT)

    print()

    print(
        "Features:",
        len(FEATURES)
    )

    print(
        "Career Categories:",
        len(CAREER_CATEGORIES)
    )

    print()

    print(
        "CAREERPATH configuration loaded successfully!"
    )
