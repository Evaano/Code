def add_grade(gradebook: dict, student_name: str, grade: int) -> dict:
    # Check if the provided grade is valid
    if grade < 0 or grade > 100:
        # If invalid return the original gradebook without changes
        print('invalid grade!')
        return gradebook
    else:
        # If the student already in the gradebook, update their grade
        if student_name in gradebook:
            gradebook[student_name] = grade
        else:
            # Adds a new entry if they're not in the gradebook
            gradebook[student_name] = grade
    return gradebook