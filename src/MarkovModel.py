import pandas as pd

class MarkovModel:
    def __init__(self, fileNames: dict):
        self.hiddenMatrix = pd.DataFrame()
        self.observedMatrix = pd.DataFrame()

    @staticmethod
    def getEntropyDifference(viterbiVal: float, probVal: float) -> float:
        pass

    def getViterbiOdState(self, destination: str) -> float:
        pass

    def getProbOfTransition(self, source: str, destination: str) -> float:
        pass

    def createRecommendation(self, previousCourses: list) -> list:
        pass


