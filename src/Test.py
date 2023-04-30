from MarkovModel import MarkovModel


class Test:
    def __init__(self, fileNames: dict):
        self.MM = MarkovModel(fileNames)
        self.confusionMatrix = [[]]

    def executeTest(self):
        pass

    def displayResults(self):
        pass
