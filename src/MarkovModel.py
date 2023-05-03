import pandas as pd
import math


class MarkovModel:
    def __init__(self, fileNames: dict):
        self.hiddenMatrix = pd.read_csv('exh.csv', sep="\t", index_col=0, na_values=['NA']).fillna(0)
        self.observedMatrix = pd.read_csv('exo.csv', sep="\t", index_col=0, na_values=['NA']).fillna(0)
        self.availableCourses = list(self.observedMatrix.columns)

    @staticmethod
    def getEntropyDifference(probVal: float, viterbiVal: float) -> float:
        eProb = -(probVal * math.log(probVal, 2))
        eViterbi = -(viterbiVal * math.log(viterbiVal, 2))
        return eViterbi - eProb

    def getViterbiOfState(self, destination: str) -> float:
        maxH = 0
        for index, row in self.hiddenMatrix.iterrows():
            if maxH < row[destination]:
                maxH = row[destination]

        maxO = 0
        for index, row in self.observedMatrix.iterrows():
            if maxO < row[destination]:
                maxO = row[destination]

        return maxH * maxO

    def valueTransition(self, source: str, destination: str) -> float:
        pH = self.hiddenMatrix[destination][source]
        pO = self.hiddenMatrix[destination][source]
        prob = pH * pO
        viterbi = self.getViterbiOfState(destination)
        return self.getEntropyDifference(prob, viterbi)

    def createRecommendation(self, previousCourses: list) -> list:
        recList = []
        for target in self.availableCourses:
            transitionValue = [0, 0]
            for prev in previousCourses:
                transitionValue[0] += self.valueTransition(prev, target)
                transitionValue[1] += 1

            recList.append([target, transitionValue[0]/transitionValue[1]])
            
        recList.sort(key=lambda x: x[1])
        return recList


if __name__ == "__main__":
    MM = MarkovModel({})
    print(MM.createRecommendation(['D', 'B']))
