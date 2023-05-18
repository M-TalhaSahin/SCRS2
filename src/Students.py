import json

class Students:
    def __init__(self):
        self.studentsDict = {}

    def addSingleCourse(self, studentId: str, courseId: str, period: (int, int), grade: float, credit: int):
        if studentId not in self.studentsDict.keys():
            self.studentsDict[studentId] = Student(studentId)
        self.studentsDict[studentId].addSingleCourse(courseId, period, grade, credit)

    def toJson(self, fileName: str):
        jsonDict = {}
        studentList = []
        singleStudentDict = {}
        semesterList = []
        singleSemesterDict = {}
        courseList = []
        courseDict = {}

        for student in self.studentsDict.keys():
            singleStudentDict.clear()
            singleStudentDict["studentId"]= self.studentsDict[student].studentId
            semesterList.clear()
            for semester in self.studentsDict[student].semesterDict.keys():
                singleSemesterDict.clear()
                p = tuple(map(int, self.studentsDict[student].semesterDict[semester].period.replace('(', '').replace(')', '').split(', ')))
                singleSemesterDict["year"] = p[0]
                singleSemesterDict["period"] = p[1]
                courseList.clear()
                for course in self.studentsDict[student].semesterDict[semester].course_grade_list:
                    courseDict.clear()
                    courseDict["courseName"] = course[0]
                    courseDict["credit"] = course[2]
                    courseDict["grade"] = course[1]
                    courseList.append(courseDict.copy())

                singleSemesterDict["courseGradeList"] = courseList.copy()
                semesterList.append(singleSemesterDict.copy())

            singleStudentDict["semesters"] = semesterList.copy()
            studentList.append(singleStudentDict.copy())

        jsonDict["students"] = studentList.copy()

        with open(fileName, 'w', encoding='utf8') as f:
            json.dump(jsonDict, f, indent=4, ensure_ascii=False)

    @classmethod
    def loadFromJson(cls, fileName: str):

        with open(fileName, 'r', encoding='utf8') as f:
            jsonDict = json.load(f)

        students = cls()

        for studentDict in jsonDict['students']:
            for semesterDict in studentDict['semesters']:
                for courseDict in semesterDict['courseGradeList']:
                    students.addSingleCourse(studentDict['studentId'], courseDict['courseName'],
                                             str((int(semesterDict['year']), int(semesterDict['period']))),
                                             courseDict['grade'], courseDict['credit'])

        return students


class Student:
    def __init__(self, _studentId: str):
        self.studentId = _studentId
        self.semesterDict = {}

    def addSingleCourse(self, courseId: str, period: (int, int), grade: float, credit: int):
        if str(period) not in self.semesterDict.keys():
            self.semesterDict[str(period)] = Semester(period)
        self.semesterDict[str(period)].course_grade_list.append([courseId, grade, credit])

    def calculateGpaBeforePeriod(self, period: (int, int)) -> float:
        sumOfP = 0
        count = 0
        for key in self.semesterDict.keys():
            if key == str(period):
                break
            for i in range(self.semesterDict[key].course_grade_list.__len__()):
                sumOfP += self.semesterDict[key].course_grade_list[i][1] * self.semesterDict[key].course_grade_list[i][2]
                count += self.semesterDict[key].course_grade_list[i][2]
        if count == 0:
            return -1
        return (sumOfP/count)


class Semester:
    def __init__(self, _period: (int, int)):
        self.period = _period
        self.course_grade_list = []  # (name: str, credit: int, grade: float)


if __name__ == "__main__":
    s = Students.loadFromJson("data/trainStudents.json")
    s.toJson("data/testing.json")

    with open('data/testing.json', 'r') as f:
        # Read the entire file as a string
        prints = f.read()

    with open('data/trainStudents.json', 'r') as f:
        # Read the entire file as a string
        old = f.read()

    if prints == old:
        print("eşit")
    else:
        print("farklı")