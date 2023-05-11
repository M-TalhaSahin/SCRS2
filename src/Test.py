import pprint

from matplotlib import pyplot as plt

from MarkovModel import MarkovModel
from Students import Students
from FileCreator import FileCreator

import pandas as pd
from sklearn import metrics

class Test:
    def __init__(self, fileNames: dict):
        self.MM = MarkovModel(fileNames)
        self.testStudents = Students.loadFromJson(fileNames['testStudentsJsonFileName'])
        self.trainStudents = Students.loadFromJson(fileNames['trainStudentsJsonFileName'])
        self.courseMatrix = pd.read_csv(fileNames['courseListCsvFileName'], index_col=0, na_values=['NA']).fillna(0).drop(columns=['KR', 'insanb']).replace(-1, 0)
        self.predList = []
        self.realList = []
        self.cutNumber = 3

    def executeTest(self):
        TSID = self.testStudents.studentsDict.keys()
        for s in TSID:
            p = self.testStudents.studentsDict[s].semesterDict[list(self.testStudents.studentsDict[s].semesterDict.keys())[0]].period
            prevp = self.prevPeriod(p)
            if prevp not in list(self.trainStudents.studentsDict[s].semesterDict.keys()):
                continue

            realValues = []
            for k in self.testStudents.studentsDict[s].semesterDict[p].course_grade_list:
                if self.courseMatrix['zor_sec'][k[0]]:
                    realValues.append(k)

            previousValues = self.trainStudents.studentsDict[s].semesterDict[prevp].course_grade_list
            predValues = self.MM.createRecommendation(self.toRawList(previousValues))
            self.setValue(realValues, predValues)
            print(1)

    def setValue(self, real, pred):
        if not real: return

        for i in range(pred.__len__()):
            pred[i] = pred[i][0]

        predP = pred[:self.cutNumber]
        predN = pred[self.cutNumber:]

        for course in real:
            if course[0] in predP:
                self.predList.append(1)
                if course[1] >= 3.5:
                    self.realList.append(1)
                else:
                    self.realList.append(0)

            if course[0] in predN:
                self.predList.append(0)
                if course[1] >= 3.5:
                    self.realList.append(1)
                else:
                    self.realList.append(0)


    @staticmethod
    def prevPeriod(period):
        tp = tuple(map(int, period.replace('(', '').replace(')', '').split(', ')))
        if tp[1] == 2:
            return str((tp[0], 1))
        else:
            return str((tp[0] - 1, 2))

    @staticmethod
    def toRawList(courseGradeList):
        rList = []
        for i in courseGradeList:
            rList.append(i[0])
        return rList

    def displayResults(self):
        confusion_matrix = metrics.confusion_matrix(self.realList, self.predList)
        Accuracy = metrics.accuracy_score(self.realList, self.predList)
        Precision = metrics.precision_score(self.realList, self.predList)
        Sensitivity_recall = metrics.recall_score(self.realList, self.predList)
        Specificity = metrics.recall_score(self.realList, self.predList, pos_label=0)
        F1_score = metrics.f1_score(self.realList, self.predList)
        print(confusion_matrix)

        pprint.pprint({"Accuracy": Accuracy, "Precision": Precision, "Sensitivity_recall": Sensitivity_recall,
                       "Specificity": Specificity, "F1_score": F1_score})
        cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=[False, True])

        cm_display.plot()
        plt.show()


if __name__ == "__main__":
    T = Test(
        {'availableInTestPeriodFileName': 'data/testAvailableCourses.csv',
         'courseListCsvFileName': 'data/courseList.csv',
         'hiddenCsvFileName': 'data/hidden.csv',
         'observedCsvFileName': 'data/observed.csv',
         'testStudentsJsonFileName': 'data/testStudents.json',
         'trainStudentsJsonFileName': 'data/trainStudents.json'})

    T.executeTest()
    T.displayResults()

