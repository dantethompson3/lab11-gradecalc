import os
import matplotlib.pyplot as plt


class Student:
    def __init__(self, name, id):
        self.name = name
        self.id = int(id)


class Assignment:
    def __init__(self, name, id, total):
        self.total = int(total)
        self.name = name
        self.id = int(id)


class Submission:
    def __init__(self, assignment, student, grade):
        self.student = int(student)
        self.assignment = int(assignment)
        self.grade = int(grade)


def get_students():
    with open("data/students.txt", "r") as file:
        students = {}
        for number in file:
            students[number[3:].strip()] = Student(number[3:].strip(), int(number[:3]))
        return students


def get_assignments():
    with open("data/assignments.txt", "r") as file:
        assignments = file.read()
        assignments = assignments.split("\n")
        assignments = [
            Assignment(*assignments[i : i + 3])
            for i in range(0, len(assignments) - 3, 3)
        ]
        assignment_dict = {}
        for assignment in assignments:
            assignment_dict[assignment.id] = assignment
        return assignment_dict


def get_submissions():
    submissions = []
    for filename in os.listdir("data/submissions"):
        with open(f"data/submissions/{filename}", "r") as file:
            student_id, assignment_id, grade = file.read().split("|")
            submissions.append(Submission(assignment_id, student_id, grade))
    return submissions


def get_menu_selection():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    print()
    return input("Enter your selection: ")


def main():
    students = get_students()
    assignments = get_assignments()
    submissions = get_submissions()
    selection = get_menu_selection()
    if selection == "1":
        name = input("What is the student's name: ")
        try:
            student = students[name]
        except KeyError:
            print("Student not found")
            return
        grade = 0
        for submission in submissions:
            if submission.student != student.id:
                continue
            grade += assignments[submission.assignment].total * (
                submission.grade / 100
            )
        print(f"{round(grade / 10)}%")
    if selection == "2" or selection == "3":
        name = input("What is the assignment name: ")
        for work in assignments.values():
            if work.name == name:
                assignment = work
                break
        else:
            print("Assignment not found")
            return
        subs = list(
            map(
                lambda hw: hw.score,
                filter(lambda hw: hw.assignment == assignment.id, submissions),
            )
        )
        if selection == "2":
            minimum = min(subs)
            average = sum(subs) // len(subs)
            maximum = max(subs)
            print(f"Min: {minimum}%")
            print(f"Avg: {average}%")
            print(f"Max: {maximum}%")

        if selection == "3":
            plt.hist(subs, bins=range(50, 101, 5))
            plt.show()


if __name__ == "__main__":
    main()
