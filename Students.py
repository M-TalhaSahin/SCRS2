
class Students:
    def __init__(self):
        self.studentsDict = {}

    def addSingleCourse(self, studentId: str, courseId: str, period: (int, int), grade: float, credit: int):
        if studentId not in self.studentsDict.keys():
            self.studentsDict[studentId] = Student(studentId)
        self.studentsDict[studentId].addSingleCourse(courseId, period, grade, credit)

    def toJson(self, fileName: str):
        pass

    @classmethod
    def loadFromJson(cls, fileName: str):
        pass


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
                count += 1
        return (sumOfP/count) if not count else -1


class Semester:
    def __init__(self, _period: (int, int)):
        self.period = _period
        self.courseGradeList = []  # (str, int, float)
