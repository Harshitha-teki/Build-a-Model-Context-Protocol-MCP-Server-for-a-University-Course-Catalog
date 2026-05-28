import sqlite3

def seed_database(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS instructors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        office TEXT,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        credits INTEGER,
        instructor_id INTEGER,
        department_id INTEGER,
        FOREIGN KEY (instructor_id) REFERENCES instructors(id),
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prerequisites (
        course_id INTEGER,
        prerequisite_id INTEGER,
        FOREIGN KEY (course_id) REFERENCES courses(id),
        FOREIGN KEY (prerequisite_id) REFERENCES courses(id),
        PRIMARY KEY (course_id, prerequisite_id)
    )''')

    # Seed data
    cursor.execute("INSERT OR IGNORE INTO departments (name, code) VALUES ('Computer Science', 'CS')")
    cursor.execute("INSERT OR IGNORE INTO departments (name, code) VALUES ('Mathematics', 'MATH')")
    cursor.execute("INSERT OR IGNORE INTO departments (name, code) VALUES ('Physics', 'PHYS')")

    cursor.execute("INSERT OR IGNORE INTO instructors (name, email, office, department_id) VALUES ('Alice Smith', 'alice@university.edu', 'Room 101', 1)")
    cursor.execute("INSERT OR IGNORE INTO instructors (name, email, office, department_id) VALUES ('Bob Johnson', 'bob@university.edu', 'Room 102', 2)")
    cursor.execute("INSERT OR IGNORE INTO instructors (name, email, office, department_id) VALUES ('Charlie Brown', 'charlie@university.edu', 'Room 103', 3)")
    cursor.execute("INSERT OR IGNORE INTO instructors (name, email, office, department_id) VALUES ('Diana Prince', 'diana@university.edu', 'Room 104', 1)")
    cursor.execute("INSERT OR IGNORE INTO instructors (name, email, office, department_id) VALUES ('Ethan Hunt', 'ethan@university.edu', 'Room 105', 2)")

    cursor.execute("INSERT OR IGNORE INTO courses (course_code, title, description, credits, instructor_id, department_id) VALUES ('CS101', 'Introduction to Programming', 'A foundational course on programming principles.', 3, 1, 1)")
    cursor.execute("INSERT OR IGNORE INTO courses (course_code, title, description, credits, instructor_id, department_id) VALUES ('CS102', 'Data Structures', 'An introduction to data structures and algorithms.', 3, 1, 1)")
    cursor.execute("INSERT OR IGNORE INTO courses (course_code, title, description, credits, instructor_id, department_id) VALUES ('MATH101', 'Calculus I', 'An introduction to differential calculus.', 4, 2, 2)")
    cursor.execute("INSERT OR IGNORE INTO courses (course_code, title, description, credits, instructor_id, department_id) VALUES ('MATH102', 'Linear Algebra', 'An introduction to linear algebra concepts.', 4, 2, 2)")
    cursor.execute("INSERT OR IGNORE INTO courses (course_code, title, description, credits, instructor_id, department_id) VALUES ('PHYS101', 'Classical Mechanics', 'An introduction to the principles of classical mechanics.', 4, 3, 3)")
    cursor.execute("INSERT OR IGNORE INTO courses (course_code, title, description, credits, instructor_id, department_id) VALUES ('CS201', 'Algorithms', 'A deeper dive into algorithms and their complexities.', 3, 1, 1)")
    cursor.execute("INSERT OR IGNORE INTO courses (course_code, title, description, credits, instructor_id, department_id) VALUES ('CS202', 'Web Development', 'Learn to build web applications.', 3, 4, 1)")
    cursor.execute("INSERT OR IGNORE INTO courses (course_code, title, description, credits, instructor_id, department_id) VALUES ('MATH201', 'Calculus II', 'Continuation of Calculus I.', 4, 2, 2)")
    cursor.execute("INSERT OR IGNORE INTO courses (course_code, title, description, credits, instructor_id, department_id) VALUES ('PHYS201', 'Electromagnetism', 'An introduction to electromagnetism.', 4, 3, 3)")
    cursor.execute("INSERT OR IGNORE INTO courses (course_code, title, description, credits, instructor_id, department_id) VALUES ('CS301', 'Machine Learning', 'An introduction to machine learning concepts.', 3, 1, 1)")

    # Add prerequisites
    cursor.execute("INSERT OR IGNORE INTO prerequisites (course_id, prerequisite_id) VALUES (2, 1)")  # Data Structures requires Introduction to Programming
    cursor.execute("INSERT OR IGNORE INTO prerequisites (course_id, prerequisite_id) VALUES (3, 1)")  # Calculus I requires Introduction to Programming
    cursor.execute("INSERT OR IGNORE INTO prerequisites (course_id, prerequisite_id) VALUES (4, 3)")  # Linear Algebra requires Calculus I
    cursor.execute("INSERT OR IGNORE INTO prerequisites (course_id, prerequisite_id) VALUES (5, 4)")  # Classical Mechanics requires Linear Algebra

    connection.commit()
    connection.close()

if __name__ == "__main__":
    seed_database('./data/catalog.db')