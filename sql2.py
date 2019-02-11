# solutions.py
"""
Adam Robertson
November 20, 2018
"""

import sqlite3 as sql

def prob1(db_file="students.db"):
    """Query the database for the list of the names of students who have a
    'B' grade in any course. Return the list.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): a list of strings, each of which is a student name.
    """
    try:
        with sql.connect(db_file) as conn:
            cur = conn.cursor()

            #Inner join on StudentInfo and StudentGrades tables
            #Query temporary table for names of students with B grades
            cur.execute("SELECT SI.StudentName FROM StudentInfo AS SI " 
                 "INNER JOIN StudentGrades AS SG ON SI.StudentID = SG.StudentID "
                 "WHERE SG.Grade == 'B';")
            names = cur.fetchall()
    finally:
        conn.close()
        result_set = []
        for n in names:
            result_set.append(n[0])
        return result_set

def prob2(db_file="students.db"):
    """Query the database for all tuples of the form (Name, MajorName, Grade)
    where 'Name' is a student's name and 'Grade' is their grade in Calculus.
    Only include results for students that are actually taking Calculus, but
    be careful not to exclude students who haven't declared a major.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    try:
        with sql.connect(db_file) as conn:
            cur = conn.cursor()

            #Left Outer Join StudentInfo and MajorInfo
            #Inner Join with Student Grades
            #Left Outer Join with CourseInfo
            #Query temporary where CourseName is 'Calculus'
            cur.execute("SELECT SI.StudentName, MI.MajorName, SG.Grade "
                        "FROM StudentInfo AS SI LEFT OUTER JOIN MajorInfo AS MI "
                        "ON SI.MajorID == MI.MajorID "
                        "INNER JOIN StudentGrades AS SG "
                        "ON SI.StudentID = SG.StudentID "
                        "LEFT OUTER JOIN CourseInfo AS CI "
                        "ON SG.CourseID == CI.CourseID "
                        "WHERE CI.CourseName == 'Calculus';")

            tuples = cur.fetchall()
    finally:
        conn.close()
        return tuples


def prob3(db_file="students.db"):
    """Query the database for the list of the names of courses that have at
    least 5 students enrolled in them.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        ((list): a list of strings, each of which is a course name.
    """
    try:
        with sql.connect(db_file) as conn:
            cur = conn.cursor()

            #Inner Join StudentGrades and CourseInfo
            #Group by CourseID
            #Return courses where enrollment is >= 5
            cur.execute("SELECT CI.CourseName "
                        "FROM StudentGrades AS SG INNER JOIN CourseInfo as CI "
                        "ON SG.CourseID == CI.CourseID "
                        "GROUP BY CI.CourseID "
                        "HAVING COUNT(*) >= 5;")
            
            tuples = cur.fetchall()
    finally:
        conn.close()
        result_set = []
        for t in tuples:
            result_set.append(t[0])
        return result_set



def prob4(db_file="students.db"):
    """Query the given database for tuples of the form (MajorName, N) where N
    is the number of students in the specified major. Sort the results in
    descending order by the counts N, then in alphabetic order by MajorName.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    try:
        with sql.connect(db_file) as conn:
            cur = conn.cursor()

            #Inner Join StudentInfo and MajorInfo
            #Group by MajorID
            #Count number of student in each major
            #Order by num_majors DESC, MajorName ASC
            cur.execute("SELECT MI.MajorName, COUNT(*) as num_majors "
                        "FROM StudentInfo as SI LEFT OUTER JOIN MajorInfo AS MI "
                        "ON SI.MajorID = MI.MajorID "
                        "GROUP BY SI.MajorID "
                        "ORDER BY num_majors DESC, MI.MajorName ASC;")

            tuples = cur.fetchall()
    finally:
        conn.close()
        return tuples


def prob5(db_file="students.db"):
    """Query the database for tuples of the form (StudentName, MajorName) where
    the last name of the specified student begins with the letter C.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    try:
        with sql.connect(db_file) as conn:
            cur = conn.cursor()

            #Outer Join StudentInfo and MajorInfo
            #Select where StudentName is like '% C$'
            cur.execute("SELECT SI.StudentName, MI.MajorName "
                        "FROM StudentInfo as SI LEFT OUTER JOIN MajorInfo AS MI "
                        "ON SI.MajorID = MI.MajorID WHERE SI.StudentName LIKE '% C%';")

            tuples = cur.fetchall()
    finally:
        conn.close()
        return tuples


def prob6(db_file="students.db"):
    """Query the database for tuples of the form (StudentName, N, GPA) where N
    is the number of courses that the specified student is in and 'GPA' is the
    grade point average of the specified student according to the following
    point system.

        A+, A  = 4.0    B  = 3.0    C  = 2.0    D  = 1.0
            A- = 3.7    B- = 2.7    C- = 1.7    D- = 0.7
            B+ = 3.4    C+ = 2.4    D+ = 1.4

    Order the results from greatest GPA to least.

    Parameters:
        db_file (str): the name of the database to connect to.

    Returns:
        (list): the complete result set for the query.
    """
    try:
        with sql.connect(db_file) as conn:
            cur = conn.cursor()

            #Inner Join StudentInfo and StudentGrades
            #Create new table with name, grade (use grades from docstring above)
            #Count number of courses
            #Calculate average gpa
            cur.execute("SELECT name, COUNT(*) as num_courses, AVG(deci_grade) AS gpa "
                        "FROM ( "
                            #New table with columns name, grade
                            "SELECT SI.StudentName AS name, CASE SG.Grade "
                                "WHEN 'A+' THEN 4.0 "
                                "WHEN 'A'THEN 4.0 "
                                "WHEN 'A-' THEN 3.7 "
                                "WHEN 'B+' THEN 3.4 "
                                "WHEN 'B' THEN 3.0 "
                                "WHEN 'B-' THEN 2.7 "
                                "WHEN 'C+' THEN 2.4 "
                                "WHEN 'C' THEN 2.0 "
                                "WHEN 'C-' THEN 1.7 "
                                "WHEN 'D+' THEN 1.4 "
                                "WHEN 'D' THEN 1.0 "
                                "WHEN 'D-' THEN 0.7 "
                                "ELSE 0 END AS deci_grade "
                            "FROM StudentInfo as SI INNER JOIN StudentGrades as SG "
                            "WHERE SI.StudentID == SG.StudentID) "
                        "GROUP BY name "
                        "ORDER BY gpa DESC;")

            tuples = cur.fetchall()
    finally:
        conn.close()
        return tuples
