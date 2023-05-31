import pandas as pd
import math


class MarkovModel:
    def __init__(self, fileNames: dict, _viterbiOff=False, _hiddenOff=False):
        self.viterbiOff = _viterbiOff
        self.hiddenOff = _hiddenOff

        self.hiddenMatrix = pd.read_csv(fileNames['hiddenCsvFileName'], index_col=0, na_values=['NA']).fillna(0).replace(-1, 0)
        self.observedMatrix = pd.read_csv(fileNames['observedCsvFileName'], index_col=0, na_values=['NA']).fillna(0).replace(-1, 0)
        self.courseMatrix = pd.read_csv(fileNames['courseListCsvFileName'], index_col=0, na_values=['NA']).fillna(0).drop(columns=['KR']).replace(-1, 0)
        self.hiddenTags = list(self.hiddenMatrix.columns)
        self.availableCourses = list(pd.read_csv(fileNames['availableInTestPeriodFileName'], header=None).values.flatten())

        self.vitH = {}
        self.vitO = {}
        self.setVit()

    def setVit(self):
        maxH = 0
        for col in list(self.hiddenMatrix.columns):
            for index, row in self.hiddenMatrix.iterrows():
                if maxH < row[col]:
                    maxH = row[col]
            self.vitH[col] = maxH
        maxO = 0
        for col in list(self.observedMatrix.columns):
            for index, row in self.observedMatrix.iterrows():
                if maxO < row[col]:
                    maxO = row[col]
            self.vitO[col] = maxO

    def getEntropyDifference(self, probVal: float, destination: str, matrixName: str) -> float:
        if self.viterbiOff:
            return probVal
        if probVal == 0:
            return 0
        viterbiVal = self.getViterbiOfState(destination, matrixName)

        eProb = -(probVal * math.log(probVal, 2))
        eViterbi = -(viterbiVal * math.log(viterbiVal, 2))  # ??????????????????????????????????????
        return eViterbi - eProb

    def getViterbiOfState(self, destination: str, matrixName: str) -> float:
        if matrixName == 'H':
            return self.vitH[destination]

        if matrixName == 'O':
            return self.vitO[destination]

        return 0

    def calculateHidden(self, source: str, destination: str) -> float:
        if self.hiddenOff:
            return 1

        sourceTagList = []
        destinationTagList = []
        destinationWeightList = []
        transDict = {}

        for tag in self.hiddenTags:
            if self.courseMatrix[tag][source]:
                sourceTagList.append(tag)
            if self.courseMatrix[tag][destination]:
                destinationTagList.append(tag)
                destinationWeightList.append(self.courseMatrix[tag][destination])

        if not (destinationTagList and sourceTagList):
            return 0

        for i in range(destinationTagList.__len__()):
            transDict[destinationTagList[i]] = (0, 0, destinationWeightList[i])
            for ts in sourceTagList:
                transDict[destinationTagList[i]] = (transDict[destinationTagList[i]][0] +
                                                    self.getEntropyDifference(self.hiddenMatrix[destinationTagList[i]][ts], destinationTagList[i], 'H'),
                                                    transDict[destinationTagList[i]][1] + 1, transDict[destinationTagList[i]][2])

            transDict[destinationTagList[i]] = (transDict[destinationTagList[i]][0] / transDict[destinationTagList[i]][1], transDict[destinationTagList[i]][2])

        val = 0
        for key in transDict.keys():
            val += transDict[key][0]*transDict[key][1]/sum(destinationWeightList)

        return val

    def valueTransition(self, source: str, destination: str) -> float:
        pH = self.calculateHidden(source, destination)
        pO = self.getEntropyDifference(self.observedMatrix[destination][source], destination, 'O')
        prob = pH * pO
        return prob

    def createRecommendation(self, previousCourses: list) -> list:
        recList = []
        for target in self.availableCourses:
            transitionValue = [0, 0]
            for prev in previousCourses:
                transitionValue[0] += self.valueTransition(prev, target)
                transitionValue[1] += 1

            recList.append([target, float(transitionValue[0]/transitionValue[1])])

        recList.sort(key=lambda x: x[1], reverse=True)
        return recList


if __name__ == "__main__":
    MM = MarkovModel(
        {'availableInTestPeriodFileName': 'data/testAvailableCourses.csv',
         'courseListCsvFileName': 'data/courseList.csv',
         'hiddenCsvFileName': 'data/hidden.csv',
         'observedCsvFileName': 'data/observed.csv',
         'testStudentsJsonFileName': 'data/testStudents.json',
         'trainStudentsJsonFileName': 'data/trainStudents.json'})

    fList = MM.createRecommendation(['152115016 VERİ TABANI YÖNETİM SİSTEMLERİ',
                                   '152115018 VERİ TABANI YÖNETİM SİSTEMLERİ LAB.',
                                   '152116009 INTRODUCTION TO MICROCOMPUTERS LAB.',
                                   '152116025 TASARIM SÜREÇLERİ',
                                   '152117008 DISTRIBUTED SYSTEMS',
                                   '152115026 YAZILIM MÜHENDİSLİĞİ',
                                   '152116008 INTRODUCTION TO MICROCOMPUTERS'])
    for i in fList:
        print(i)