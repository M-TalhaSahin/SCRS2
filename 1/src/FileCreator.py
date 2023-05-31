import pandas as pd
import numpy as np
import csv
from Students import Students


class FileCreator:
    def __init__(self):
        self.hiddenCsvFileName = "data/hidden.csv"
        self.observedCsvFileName = "data/observed.csv"
        self.courseListCsvFileName = "data/courseList.csv"
        self.trainStudentsJsonFileName = "data/trainStudents.json"
        self.testStudentsJsonFileName = "data/testStudents.json"
        self.availableInTestPeriodFileName = "data/testAvailableCourses.csv"
        self.createdTagsFileName = "data/createdTags.csv"
        self.extraTags = 1

    def getFileNames(self) -> dict:
        return {"hiddenCsvFileName": self.hiddenCsvFileName,
                "observedCsvFileName": self.observedCsvFileName,
                "courseListCsvFileName": self.courseListCsvFileName,
                "trainStudentsJsonFileName": self.trainStudentsJsonFileName,
                "testStudentsJsonFileName": self.testStudentsJsonFileName,
                "availableInTestPeriodFileName": self.availableInTestPeriodFileName}

    def createFilesFrom(self, brmOgrDersFileName: str, brmDersFileName: str, testPeriod: (int, int), createdTagsFileName: str):
        courseNameCreditDict, courseNameCreditDictElective = self.getCourseList(brmDersFileName, createdTagsFileName, testPeriod)
        train = self.getStudentsObjects(brmOgrDersFileName, testPeriod, courseNameCreditDict)
        self.createMatrixes(train, courseNameCreditDict, courseNameCreditDictElective)

    def getCourseList(self, brmDersFileName: str, createdTagsFileName: str, testPeriod: (int, int)) -> (dict, dict):
        excel_data = pd.read_excel(brmDersFileName, dtype=str).fillna("0")
        createdTagList =  pd.read_csv(createdTagsFileName, index_col=0, na_values=['NA'], encoding='utf-8-sig').fillna(0)
        # print(createdTagList['algorithms']['152111001 CALCULUS I'])
        testCourseNames = []
        courseList_dict = {}
        electiveCourseList_dict = {}
        with open(self.courseListCsvFileName, mode="w", newline="", encoding='utf-8-sig') as dosya:
            yazici = csv.writer(dosya)
            yazici.writerow(['COURSENAME', 'KR', 'zor_sec', 'tembil', 'meslek', 'insanb', 'tas', 'algorithms','dataStructures',
                             'artificialIntelligence',"machineLearning","computerNetworks","databases", "operatingSystems","softwareEngineering",
                             "computerGraphics","cybersecurity","humanComputerInteraction","webDevelopment","programmingLanguages","computerVision",
                             "naturalLanguageProcessing","hardwareDesign"])

            for index, row in excel_data.iterrows():
                lesson_code = row['DERS_KODU']
                # Get values for each DERSKODU key
                if lesson_code not in courseList_dict:
                    if row['KR'] != "0" and row['INSANB'] == "0" and "S&D" not in row['DERSADI'] and "ENGINEERING RESEARCH ON" not in row['DERSADI']:
                        courseList_dict[lesson_code] = {
                            'ders_adi': row['DERSADI'],
                            'kr': row['KR'],
                            'zor_sec': row['ZORSEC'],
                            'tembil': row['TEMBIL'],
                            'meslek': row['MESLEK'],
                            'tas': row['TASARIM']
                        }

                        for column in createdTagList.columns:
                            info = float(createdTagList[column][lesson_code + " " + row['DERSADI']]) * self.extraTags
                            courseList_dict[lesson_code][column] = info

                        courseList_dict[lesson_code] = self.normalizeCourseDict(courseList_dict[lesson_code])
                        rowtowrite = [lesson_code + " " + row['DERSADI']]
                        for column in list(courseList_dict[lesson_code].keys())[1:]:
                            info = float(courseList_dict[lesson_code][column])
                            rowtowrite.append(info)
                        yazici.writerow(rowtowrite)

                        if courseList_dict[lesson_code]['zor_sec'] != "0":
                            electiveCourseList_dict[lesson_code] = {
                                'ders_adi': row['DERSADI'],
                                'kr': row['KR'],
                                'zor_sec': row['ZORSEC'],
                                'tembil': row['TEMBIL'],
                                'meslek': row['MESLEK'],
                                'tas': row['TASARIM']
                            }
                            for column in createdTagList.columns:
                                electiveCourseList_dict[lesson_code][column] = float(createdTagList[column][lesson_code + " " + row['DERSADI']]) * self.extraTags
                            electiveCourseList_dict[lesson_code] = self.normalizeCourseDict(electiveCourseList_dict[lesson_code])

                if lesson_code + " " + row['DERSADI'] not in testCourseNames:
                    if row['KR'] != "0" and row['INSANB'] == "0" and "S&D" not in row['DERSADI'] and "ENGINEERING RESEARCH ON" not in row['DERSADI']:
                        if courseList_dict[lesson_code]['zor_sec'] != "0":
                            if (int(row['ACILDIGI_YIL']), int(row['ACILDIGI_DONEM'])) == testPeriod:
                                testCourseNames.append(lesson_code + " " + row['DERSADI'])

            dosya.close()

        with open(self.availableInTestPeriodFileName, mode="w", newline="", encoding='utf-8-sig') as f:
            csvw = csv.writer(f)
            for c in testCourseNames:
                csvw.writerow([c])

        return courseList_dict, electiveCourseList_dict  # return courseList as a dictionary

    def getStudentsObjects(self, brmOgrDersFileName: str, testPeriod: (int, int), courseNameCreditDict: dict) -> Students:
        sTrain = Students()
        sTest = Students()
        excel_data = pd.read_excel(brmOgrDersFileName, dtype=str)  # Read Excel data

        for index, row in excel_data.iterrows():
            if row['DERS_KODU'] not in courseNameCreditDict.keys():
                continue

            if row['YIL'] == str(testPeriod[0]) and row['DONEM'] == str(testPeriod[1]):
                sTest.addSingleCourse(row['OGRNO'], row['DERS_KODU'] + " " + courseNameCreditDict[row['DERS_KODU']]['ders_adi'],
                                      str(testPeriod), float(row['SAYISAL']), int(courseNameCreditDict[row['DERS_KODU']]['kr']))

            else:
                sTrain.addSingleCourse(row['OGRNO'], row['DERS_KODU'] + " " + courseNameCreditDict[row['DERS_KODU']]['ders_adi'],
                                       str((int(row['YIL']), int(row['DONEM']))), float(row['SAYISAL']), int(courseNameCreditDict[row['DERS_KODU']]['kr']))

        sTrain.toJson(self.trainStudentsJsonFileName)
        sTest.toJson(self.testStudentsJsonFileName)
        return sTrain

    def createMatrixes(self, sTrain: Students, courseNamesDict: dict, electiveCourseNamesDict):
        x = courseNamesDict.keys().__len__()
        y = electiveCourseNamesDict.keys().__len__()
        cn = []
        ecn = []
        all_courses_index_dict = {}
        elective_courses_index_dict = {}
        index = 0
        for k in courseNamesDict.keys():
            all_courses_index_dict[k + " " + courseNamesDict[k]['ders_adi']] = index
            cn.append(k + " " + courseNamesDict[k]['ders_adi'])
            index += 1
        index = 0
        for k in electiveCourseNamesDict.keys():
            elective_courses_index_dict[k + " " + electiveCourseNamesDict[k]['ders_adi']] = index
            ecn.append(k + " " + electiveCourseNamesDict[k]['ders_adi'])
            index += 1

        hiddenIndex = {'tembil': 0, 'meslek': 1, 'tas': 2, 'algorithms': 3,
                       'dataStructures':4, 'artificialIntelligence':5, 'machineLearning':6,
                       'computerNetworks':7, 'databases':8, 'operatingSystems':9,
                       'softwareEngineering':10, 'computerGraphics':11, 'cybersecurity':12,
                       'humanComputerInteraction':13, 'webDevelopment':14, 'programmingLanguages':15,
                       'computerVision':16, 'naturalLanguageProcessing':17, 'hardwareDesign':18}

        passesMx = np.zeros((x, y))
        countMx = np.zeros((x, y))

        titleMx = np.zeros((19, 19))  # title size
        countHiddenMx = np.zeros((19, 19))  # title counter

        for keyStu in sTrain.studentsDict.keys():
            keys = sTrain.studentsDict[keyStu].semesterDict.keys()
            for sem1i in range(keys.__len__() - 1):
                key = list(keys)[sem1i]
                nextKey = FileCreator.nextPeriod(key)
                for if2 in range(2):
                    if nextKey in keys:
                        for i in range(sTrain.studentsDict[keyStu].semesterDict[key].course_grade_list.__len__()):
                            for j in range(sTrain.studentsDict[keyStu].semesterDict[nextKey].course_grade_list.__len__()):
                                s1 = sTrain.studentsDict[keyStu].semesterDict[key].course_grade_list[i][0]
                                s2 = sTrain.studentsDict[keyStu].semesterDict[nextKey].course_grade_list[j][0]
                                if s1 in cn and s2 in ecn:
                                    pass_val = FileCreator.isSuccessStatic(sTrain.studentsDict[keyStu].semesterDict[nextKey].course_grade_list[j][1])
                                    passesMx[all_courses_index_dict[s1]][elective_courses_index_dict[s2]] += int(pass_val)
                                    countMx[all_courses_index_dict[s1]][elective_courses_index_dict[s2]] += 1

                                    s1Title = {}
                                    s2Title = {}

                                    for ckey in list(courseNamesDict[s1.split(' ')[0]].keys())[3:]:
                                        s1Title[ckey] = 1 if 0 != float(courseNamesDict[s1.split(' ')[0]][ckey]) else 0

                                    kr = int(courseNamesDict[s2.split(' ')[0]]['kr'])

                                    top = 0
                                    for ckey in list(courseNamesDict[s1.split(' ')[0]].keys())[3:]:
                                        s2Title[ckey] = courseNamesDict[s2.split(' ')[0]][ckey]
                                        top += s2Title[ckey]

                                    singlePoint = (kr / top if top else 0)
                                    # edit singlepoint for created and default tags
                                    for f1 in s1Title.keys():
                                        for f2 in s2Title.keys():
                                            if s1Title[f1] != 0 and s2Title[f2] != 0:
                                                val = singlePoint * s2Title[f2]
                                                titleMx[hiddenIndex[f1]][hiddenIndex[f2]] += val*pass_val
                                                countHiddenMx[hiddenIndex[f1]][hiddenIndex[f2]] += 1
                                    #courseNamesDict[s1.split(' ')[0]][k]
                    nextKey = FileCreator.next2Period(key)

        print(1)
        finalMx = np.zeros((x, y))
        finalHiddenMx = np.zeros((19, 19))

        for i in range(x):
            for j in range(y):
                if countMx[i][j] == 0:
                    finalMx[i][j] = -1
                else:
                    finalMx[i][j] = passesMx[i][j] / countMx[i][j]

        for i in range(19):
            for j in range(19):
                if countHiddenMx[i][j] == 0:
                    finalHiddenMx[i][j] = -1
                else:
                    finalHiddenMx[i][j] = titleMx[i][j] / countHiddenMx[i][j]

        finalMx = FileCreator.normalizeMx(finalMx)
        finalHiddenMx = FileCreator.normalizeMx(finalHiddenMx)

        df = pd.DataFrame(index=list(hiddenIndex.keys()), columns=list(hiddenIndex.keys()), data=finalHiddenMx)
        df.to_csv(self.hiddenCsvFileName, encoding='utf-8-sig')

        df = pd.DataFrame(index=cn, columns=ecn, data=finalMx)
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

    @staticmethod
    def isSuccessStatic(grade):
        if grade >= 3.0:
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
    FC.createFilesFrom("resources/BrmOgrDers.xls", "resources/BrmDers.xls", (2018, 2), "resources/x.csv")
    pprint.pprint(FC.getFileNames())
