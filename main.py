import json
import os
import time

DATA_FILE = "students.json"


def create_data_file_if_missing():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump([], file)


def load_students():
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_students(students):
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


def login():
    username = "admin"
    password = "password"

    while True:
        given_username = input("Enter username: ")
        given_password = input("Enter password: ")

        if given_username == username and given_password == password:
            print("Login successful.")
            break
        else:
            print("Incorrect username or password. Please try again.")


def add_student():
    student_number = input("Enter student number: ")
    name = input("Enter student name: ")
    contact = input("Enter student contact information: ")

    students = load_students()

    duplicate_found = False
    for student in students:
        if student["student_number"] == student_number:
            duplicate_found = True

    if duplicate_found:
        print("Student number already exists.")
        return

    new_student = {
        "student_number": student_number,
        "name": name,
        "contact": contact,
        "grades": []
    }

    students.append(new_student)
    save_students(students)

    print("Student added.")


def add_grade():
    student_number = input("Enter student number: ")
    course = input("Enter course name: ")
    grade = input("Enter grade: ")

    students = load_students()

    student_found = False

    for student in students:
        if student["student_number"] == student_number:
            student["grades"].append({
                "course": course,
                "grade": grade
            })
            student_found = True
            break

    if student_found:
        save_students(students)
        print("Grade added.")
    else:
        print("Student not found.")


def search_student():
    student_number = input("Enter student number to search for: ")

    start_time = time.perf_counter()

    students = load_students()

    found_student = None

    for student in students:
        if student["student_number"] == student_number:
            found_student = student

    end_time = time.perf_counter()

    if found_student:
        print("Student found:")
        print(f"Student Number: {found_student['student_number']}")
        print(f"Name: {found_student['name']}")
        print(f"Contact: {found_student['contact']}")
        print(f"Grades: {found_student['grades']}")
    else:
        print("Student not found.")

    print(f"Search took {end_time - start_time:.6f} seconds.")


def display_all_students():
    students = load_students()

    if not students:
        print("No students found.")
        return

    print("All students:")

    for i in range(len(students)):
        sorted_students = sorted(students, key=lambda student: student["name"])
        student = sorted_students[i]

        print(f"Student Number: {student['student_number']}")
        print(f"Name: {student['name']}")
        print(f"Contact: {student['contact']}")
        print(f"Grades: {student['grades']}")
        print()


def count_total_grades():
    students = load_students()

    total = 0

    for student in students:
        for grade in student["grades"]:
            total += 1

    print(f"Total number of grades: {total}")


def display_course_summary():
    students = load_students()

    all_courses = []

    # Inefficient: builds a course list using repeated membership checks
    for student in students:
        for grade in student["grades"]:
            if grade["course"] not in all_courses:
                all_courses.append(grade["course"])

    print("Course summary:")

    # Inefficient: nested loops repeatedly scan all students and grades
    for course in all_courses:
        count = 0

        for student in students:
            for grade in student["grades"]:
                if grade["course"] == course:
                    count += 1

        print(f"{course}: {count} grade(s)")


def save_backup():
    students = load_students()

    json_text = json.dumps(students)
    copied_students = json.loads(json_text)

    with open("students_backup.json", "w") as file:
        json.dump(copied_students, file, indent=4)

    print("Backup saved.")


def main():
    create_data_file_if_missing()
    login()

    while True:
        print("\nSelect an action:")
        print("1. Add a student")
        print("2. Add grade")
        print("3. Search for student")
        print("4. Display all students")
        print("5. Count total grades")
        print("6. Display course summary")
        print("7. Save backup")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_grade()
        elif choice == "3":
            search_student()
        elif choice == "4":
            display_all_students()
        elif choice == "5":
            count_total_grades()
        elif choice == "6":
            display_course_summary()
        elif choice == "7":
            save_backup()
        elif choice == "8":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
