import pandas as pd
import numpy as np
import csv
from Students import Students

PASS_GRADE = 3.0
STATIC = 1
PCON = 1


class FileCreator:
    def __init__(self):
        self.hiddenCsvFileName = "data/hidden.csv"
        self.observedCsvFileName = "data/observed.csv"
        self.courseListCsvFileName = "data/courseList.csv"
        self.trainStudentsJsonFileName = "data/trainStudents.json"
        self.testStudentsJsonFileName = "data/testStudents.json"
        self.availableInTestPeriodFileName = "data/testAvailableCourses.csv"
        self.createdTagsFileName = "data/createdTags.csv"
        self.codeNameMap = {}
        self.passGrade = PASS_GRADE
        self.PCon = PCON

    def getFileNames(self) -> dict:
        return {"hiddenCsvFileName": self.hiddenCsvFileName,
                "observedCsvFileName": self.observedCsvFileName,
                "courseListCsvFileName": self.courseListCsvFileName,
                "trainStudentsJsonFileName": self.trainStudentsJsonFileName,
                "testStudentsJsonFileName": self.testStudentsJsonFileName,
                "availableInTestPeriodFileName": self.availableInTestPeriodFileName}

    def createFilesFrom(self, brmOgrDersFileName: str, brmDersFileName: str, testPeriod: (int, int), createdTagsFileName: str):
        print("Creating course list.......")
        courseNameCreditDict, courseNameCreditDictElective = self.getCourseList(brmDersFileName, createdTagsFileName, testPeriod)
        print("Creating student objects...")
        train = self.getStudentsObjects(brmOgrDersFileName, testPeriod, courseNameCreditDict)
        print("Creating matrices..........")
        self.createMatrices(train, courseNameCreditDict, courseNameCreditDictElective)

    def getCourseList(self, brmDersFileName: str, createdTagsFileName: str, testPeriod: (int, int)) -> (dict, dict):
        excel_data = pd.read_excel(brmDersFileName, dtype=str).fillna("0")

        courseList_dict = {}
        electiveCourseList_dict = {}

        with open(self.courseListCsvFileName, mode="w", newline="", encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            firstRow = ['DERSADI', 'KR', 'ZORSEC']

            if self.PCon:
                for i in range(1, 12, 1):
                    firstRow.append("PC" + i.__str__())
            else:
                firstRow += ["TASARIM", "MESLEK", "TEMBIL"]

            writer.writerow(firstRow)

            for index, row in excel_data.iterrows():  # brmDers must be sorted by year and period
                self.codeNameMap[row["DERS_KODU"]] = row['DERSADI']
                if row["DERS_KODU"] == "152118635":
                    continue
                if row['KR'] != "0" and row['INSANB'] == "0" and "S&D" not in row['DERSADI'] and "ENGINEERING RESEARCH ON" not in row['DERSADI']:
                    tempDict = {row['DERSADI']: {}}
                    tempElectiveDict = {row['DERSADI']: {}}

                    for keyIndex in range(1, firstRow.__len__(), 1):
                        tempDict[row['DERSADI']][firstRow[keyIndex]] = row[firstRow[keyIndex]]

                        if row['ZORSEC'] != "0":
                            tempElectiveDict[row['DERSADI']][firstRow[keyIndex]] = row[firstRow[keyIndex]]

                    if row['DERSADI'] in courseList_dict.keys():
                        courseList_dict.update(tempDict)
                    else:
                        courseList_dict[row['DERSADI']] = tempDict[row['DERSADI']]

                    if row['ZORSEC'] != "0":
                        if row['DERSADI'] in electiveCourseList_dict.keys():
                            electiveCourseList_dict.update(tempElectiveDict)
                        else:
                            electiveCourseList_dict[row['DERSADI']] = tempElectiveDict[row['DERSADI']]

            for course in courseList_dict.keys():
                rowToWrite = [course]
                for courseKey in courseList_dict[course]:
                    rowToWrite.append(courseList_dict[course][courseKey])
                writer.writerow(rowToWrite)  # write somewhere else dude

            availableInTestPeriod = []
            for index, row in excel_data.iterrows():
                if (int(row['ACILDIGI_YIL']), int(row['ACILDIGI_DONEM'])) == testPeriod and row['ZORSEC'] != "0" and row['KR'] != "0" and row['INSANB'] == "0" \
                        and "S&D" not in row['DERSADI'] and "ENGINEERING RESEARCH ON" not in row['DERSADI'] and "MÜH. ARAŞTIRMALARI" not in row['DERSADI']:
                    availableInTestPeriod.append(row['DERSADI'])

            file.close()

        with open(self.availableInTestPeriodFileName, mode="w", newline="", encoding='utf-8-sig') as f:
            csvw = csv.writer(f)
            for c in availableInTestPeriod:
                csvw.writerow([c])

        return courseList_dict, electiveCourseList_dict

    def getStudentsObjects(self, brmOgrDersFileName: str, testPeriod: (int, int), courseNameCreditDict: dict) -> Students:
        sTrain = Students()
        sTest = Students()
        excel_data = pd.read_excel(brmOgrDersFileName, dtype=str)

        for index, row in excel_data.iterrows():
            if self.codeNameMap[row['DERS_KODU']] not in courseNameCreditDict.keys():
                continue

            no, cid, period = row['OGRNO'], self.codeNameMap[row['DERS_KODU']], str((int(row['YIL']), int(row['DONEM'])))
            grade, kr = float(row['SAYISAL']), int(courseNameCreditDict[self.codeNameMap[row['DERS_KODU']]]['KR'])

            if (int(row['YIL']), int(row['DONEM'])) == testPeriod:
                sTest.addSingleCourse(no, cid, period, grade, kr)
            else:
                sTrain.addSingleCourse(no, cid, period, grade, kr)

        sTrain.toJson(self.trainStudentsJsonFileName)
        sTest.toJson(self.testStudentsJsonFileName)
        return sTrain

    def createMatrices(self, sTrain: Students, courseNamesDict: dict, electiveCourseNamesDict):
        # INITIALIZATIONS
        obsx = courseNamesDict.keys().__len__()
        obsy = electiveCourseNamesDict.keys().__len__()
        allIndex = {}
        electiveIndex = {}

        index = 0
        allCourseNames = []
        for k in courseNamesDict.keys():
            allIndex[k] = index
            allCourseNames.append(k)
            index += 1

        index = 0
        electiveCourseNames = []
        for k in electiveCourseNamesDict.keys():
            electiveIndex[k] = index
            electiveCourseNames.append(k)
            index += 1

        hiddenIndex = {}
        if self.PCon:
            for i in range(1, 12, 1):
                hiddenIndex[f'PC{i}'] = i - 1
        else:
            fr = ["TASARIM", "MESLEK", "TEMBIL"]
            for i in range(fr.__len__()):
                hiddenIndex[fr[i]] = i

        observedValueMx = np.zeros((obsx, obsy))
        observedCountMx = np.zeros((obsx, obsy))

        hidxy = hiddenIndex.__len__()
        hiddenValueMx = np.zeros((hidxy, hidxy))
        hiddenCountMx = np.zeros((hidxy, hidxy))

        # INITIALIZATIONS END

        for currentStudent in sTrain.studentsDict.values():
            semesterKeys = currentStudent.semesterDict.keys()
            for semester1 in range(semesterKeys.__len__() - 1):
                keySemester1 = list(semesterKeys)[semester1]
                keySemester2 = self.nextPeriod(keySemester1)
                for runTwice in range(2):  # run for next 2 periods
                    if keySemester2 in semesterKeys:
                        for courseGrade1 in currentStudent.semesterDict[keySemester1].course_grade_list:
                            for courseGrade2 in currentStudent.semesterDict[keySemester2].course_grade_list:
                                course1 = courseGrade1[0]
                                course2 = courseGrade2[0]

                                if course1 in allCourseNames and course2 in electiveCourseNames:
                                    if STATIC:
                                        transitionSuccess = self.isSuccessStatic(courseGrade2[1], currentStudent.calculateGpaBeforePeriod(keySemester2))
                                    else:
                                        transitionSuccess = self.isSuccessDynamic(courseGrade2[1], currentStudent.calculateGpaBeforePeriod(keySemester2))

                                    # OBSERVED
                                    observedValueMx[allIndex[course1]][electiveIndex[course2]] += int(transitionSuccess)
                                    observedCountMx[allIndex[course1]][electiveIndex[course2]] += 1

                                    # HIDDEN
                                    course1Controls = {}
                                    course2Values = {}

                                    sumOfWeights = 0
                                    for hiddenKey in list(hiddenIndex.keys()):
                                        course1Controls[hiddenKey] = 1 if 0 != float(courseNamesDict[course1][hiddenKey]) else 0
                                        course2Values[hiddenKey] = float(courseNamesDict[course2][hiddenKey])
                                        sumOfWeights += course2Values[hiddenKey]

                                    singlePoint = ((int(courseNamesDict[course2]['KR']) / sumOfWeights) if sumOfWeights else 0)

                                    for c1Control in course1Controls.keys():
                                        for c2Value in course2Values.keys():
                                            if course1Controls[c1Control] != 0 and course2Values[c2Value] != 0:
                                                weightedValue = singlePoint * course2Values[c2Value]
                                                hiddenValueMx[hiddenIndex[c1Control]][hiddenIndex[c2Value]] += weightedValue * transitionSuccess
                                                hiddenCountMx[hiddenIndex[c1Control]][hiddenIndex[c2Value]] += 1

                    keySemester2 = FileCreator.nextPeriod(keySemester2)


        print(1)
        finalObservedMx = np.zeros((obsx, obsy))
        finalHiddenMx = np.zeros((hidxy, hidxy))

        for i in range(obsx):
            for j in range(obsy):
                if observedCountMx[i][j] == 0:
                    finalObservedMx[i][j] = 0
                else:
                    finalObservedMx[i][j] = observedValueMx[i][j] / observedCountMx[i][j]

        for i in range(hidxy):
            for j in range(hidxy):
                if hiddenCountMx[i][j] == 0:
                    finalHiddenMx[i][j] = 0
                else:
                    finalHiddenMx[i][j] = hiddenValueMx[i][j] / hiddenCountMx[i][j]

        finalObservedMx = FileCreator.normalizeMx(finalObservedMx)
        finalHiddenMx = FileCreator.normalizeMx(finalHiddenMx)

        df = pd.DataFrame(index=list(hiddenIndex.keys()), columns=list(hiddenIndex.keys()), data=finalHiddenMx)
        df.to_csv(self.hiddenCsvFileName, encoding='utf-8-sig')

        df = pd.DataFrame(index=allCourseNames, columns=electiveCourseNames, data=finalObservedMx)
        df.to_csv(self.observedCsvFileName, encoding='utf-8-sig')

    @staticmethod
    def nextPeriod(period):  # "(2022, 1)"
        tp = tuple(map(int, period.replace('(', '').replace(')', '').split(', ')))
        if tp[1] == 1:
            return str((tp[0], 2))
        else:
            return str((tp[0] + 1, 1))

    @staticmethod
    def next2Period(period):
        tp = tuple(map(int, period.replace('(', '').replace(')', '').split(', ')))
        return str((tp[0] + 1, tp[1]))

    def isSuccessStatic(self, grade, gpa):
        if grade >= self.passGrade:
            return 1
        else:
            return 0

    def isSuccessDynamic(self, grade, gpa):
        if gpa >= 2:
            if grade >= 1:
                return 1
            else:
                return 0
        else:
            if grade >= 2:
                return 1
            else:
                return 0

    @staticmethod
    def normalizeMx(mx):
        x = mx.shape[0]  # 1  325
        y = mx.shape[1]  # ?  5
        for i in range(x):
            temp = np.zeros((1, y))
            sumOfAll = 0
            for j in range(y):
                val = mx[i][j]
                if val != 0 and val != -1:
                    sumOfAll += val
            if sumOfAll == 0:
                continue
            for j in range(y):
                val = mx[i][j]
                if val != 0 and val != -1:
                    temp[0][j] = val / sumOfAll
                else:
                    temp[0][j] = val
            mx[i] = temp
        return mx

    @staticmethod
    def normalizeCourseDict(courseDict):
        base = list(courseDict.keys())[3:6]
        created = list(courseDict.keys())[6:]
        sumofval = 0
        for key in base:
            sumofval += float(courseDict[key])
        for key in base:
            courseDict[key] = ((float(courseDict[key]) / sumofval) if sumofval else 0)
        sumofval = 0
        for key in created:
            sumofval += float(courseDict[key])
        for key in created:
            courseDict[key] = ((float(courseDict[key]) / sumofval) if sumofval else 0)
        return courseDict


if __name__ == "__main__":
    import pprint
    FC = FileCreator()
    FC.createFilesFrom("resources/BrmOgrDers.xls", "resources/BrmDersCf.xls", (2018, 2), "resources/x.csv")
    pprint.pprint(FC.getFileNames())
