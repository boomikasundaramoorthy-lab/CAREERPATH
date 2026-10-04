from database import get_connection, create_database


def add_sample_data():
    create_database()

    connection = get_connection()
    cursor = connection.cursor()

    # Jobs
    jobs = [
        (
            "Junior Web Developer",
            "Tech Solutions",
            "Chennai",
            "Full Time",
            "Build and maintain responsive websites.",
            "HTML,CSS,JavaScript"
        ),
        (
            "Python Developer Intern",
            "Digital Works",
            "Bangalore",
            "Internship",
            "Work on Python-based applications.",
            "Python,SQL,Git"
        ),
        (
            "Data Analyst Intern",
            "Data Insights",
            "Chennai",
            "Internship",
            "Analyze data and create useful reports.",
            "Python,SQL,Excel"
        ),
        (
            "UI/UX Design Intern",
            "Creative Studio",
            "Coimbatore",
            "Internship",
            "Design user-friendly digital experiences.",
            "Figma,UI Design,UX"
        ),
        (
            "Cyber Security Intern",
            "SecureTech",
            "Hyderabad",
            "Internship",
            "Learn security monitoring and basic testing.",
            "Networking,Linux,Security"
        ),
        (
            "AI/ML Intern",
            "AI Innovations",
            "Bangalore",
            "Internship",
            "Work with machine learning concepts and projects.",
            "Python,Machine Learning,Data Science"
        )
    ]

    for job in jobs:
        cursor.execute("""
            INSERT INTO jobs
            (title, company, location, job_type, description, skills)
            SELECT ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM jobs
                WHERE title = ? AND company = ?
            )
        """, job + (job[0], job[1]))

    # Courses
    courses = [
        (
            "Web Development",
            "Web Development",
            "Beginner",
            "3 Months",
            "Learn HTML, CSS and JavaScript."
        ),
        (
            "Python Programming",
            "Programming",
            "Beginner",
            "2 Months",
            "Learn Python programming from basics."
        ),
        (
            "Data Science",
            "Data Science",
            "Intermediate",
            "4 Months",
            "Learn data analysis and visualization."
        ),
        (
            "AI & Machine Learning",
            "Artificial Intelligence",
            "Advanced",
            "5 Months",
            "Learn machine learning concepts and projects."
        ),
        (
            "UI/UX Design",
            "Design",
            "Beginner",
            "2 Months",
            "Learn UI/UX design and Figma."
        ),
        (
            "Cyber Security",
            "Cyber Security",
            "Intermediate",
            "4 Months",
            "Learn networking and cyber security basics."
        )
    ]

    for course in courses:
        cursor.execute("""
            INSERT INTO courses
            (title, category, level, duration, description)
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM courses
                WHERE title = ?
            )
        """, course + (course[0],))

    connection.commit()
    connection.close()

    print("CAREERPATH sample data added successfully!")


if __name__ == "__main__":
    add_sample_data()
