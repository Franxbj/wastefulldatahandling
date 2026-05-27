import json
import os
import time

# file where all student data is stored
DATA_FILE = "students.json"


def create_data_file_if_missing():
    # check if the data file exists, if not create an empty one
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            json.dump([], file)


def load_students():
    # open the data file and return all students as a list
    with open(DATA_FILE, "r") as file:
        return json.load(file)


def save_students(students):
    # write the updated student list back to the data file
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


def login():
    # hardcoded credentials for simplicity
    username = "admin"
    password = "password"

    # keep asking until correct credentials are entered
    while True:
        given_username = input("Enter username: ")
        given_password = input("Enter password: ")

        if given_username == username and given_password == password:
            print("Login successful.")
            break
        else:
            print("Incorrect username or password. Please try again.")


def add_student():
    # get new student details from user
    student_number = input("Enter student number: ")
    name = input("Enter student name: ")
    contact = input("Enter student contact information: ")

    # load existing students from file
    students = load_students()

    # check if student number already exists
    duplicate_found = False
    for student in students:
        if student["student_number"] == student_number:
            duplicate_found = True
            break # stop looping once duplicate is found

    if duplicate_found:
        print("Student number already exists.")
        return

    # create a new student record with an empty grades list
    new_student = {
        "student_number": student_number,
        "name": name,
        "contact": contact,
        "grades": []
    }

    # add the new student and save to file
    students.append(new_student)
    save_students(students)

    print("Student added.")


def add_grade():
    # get grade details from user
    student_number = input("Enter student number: ")
    course = input("Enter course name: ")
    grade = input("Enter grade: ")

    # load existing students from file
    students = load_students()

    student_found = False

    # find the student and append the new grade
    for student in students:
        if student["student_number"] == student_number:
            student["grades"].append({
                "course": course,
                "grade": grade
            })
            student_found = True
            break # stop looping once student is found

    if student_found:
        save_students(students)
        print("Grade added.")
    else:
        print("Student not found.")


def search_student():
    student_number = input("Enter student number to search for: ")

    # start timer to measure search performance
    start_time = time.perf_counter()

    # load existing students from file
    students = load_students()

    found_student = None

    # search for the student by student number
    for student in students:
        if student["student_number"] == student_number:
            found_student = student
            break # stop looping once a student is found

    # stop timer
    end_time = time.perf_counter()

    if found_student:
        print("Student found:")
        print(f"Student Number: {found_student['student_number']}")
        print(f"Name: {found_student['name']}")
        print(f"Contact: {found_student['contact']}")
        print(f"Grades: {found_student['grades']}")
    else:
        print("Student not found.")

    # display how long the search took
    print(f"Search took {end_time - start_time:.6f} seconds.")


def display_all_students():
    # load existing students from file
    students = load_students()

    if not students:
        print("No students found.")
        return

    print("All students:")

    # sort the list once before looping
    sorted_students = sorted(students, key=lambda student: student["name"])

    # loop over the already sorted list
    for student in sorted_students:
        print(f"Student Number: {student['student_number']}")
        print(f"Name: {student['name']}")
        print(f"Contact: {student['contact']}")
        print(f"Grades: {student['grades']}")
        print()


def count_total_grades():
    # load existing students from file
    students = load_students()

    total = 0

    # count all grades across all students
    for student in students:
        for grade in student["grades"]:
            total += 1

    print(f"Total number of grades: {total}")


def display_course_summary():
    # load existing students from file
    students = load_students()

    #dictionary to store each course and its grade count
    course_counts = {}

    # single loop through all students and grades
    for student in students:
        for grade in student["grades"]:
            course = grade["course"]
            # if course is new, add it to the dictionary with a count of 0
            if course not in course_counts:
                course_counts[course] = 0
            # increment the count for this course
            course_counts[course] += 1

    print("Course summary:")

    # loop through the dictionary and print each course and its count
    for course, count in course_counts.items():
        
        print(f"{course}: {count} grade(s)")


def save_backup():
    # load existing students from file
    students = load_students()

    # write directly to file without unnecessary serilization
    with open("students_backup.json", "w") as file:
        json.dump(students, file, indent=4)

    print("Backup saved.")


def main():
     # create the data file if it doesn't exist
    create_data_file_if_missing()

    # prompt user to login before accessing the system
    login()

    # main menu loop
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
