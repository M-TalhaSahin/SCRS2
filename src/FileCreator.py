import pandas as pd

from Students import Students


class FileCreator:
    def __init__(self):
        self.hiddenCsvFileName = "hidden.csv"
        self.observedCsvFileName = "observed.csv"
        self.courseListCsvFileName = "courseList.csv"
        self.trainStudentsJsonFileName = "trainStudents.json"
        self.testStudentsJsonFileName = "testStudents.json"

    def getFileNames(self) -> dict:
        return {"hiddenCsvFileName": self.hiddenCsvFileName,
                "observedCsvFileName": self.observedCsvFileName,
                "courseListCsvFileName": self.courseListCsvFileName,
                "trainStudentsJsonFileName": self.trainStudentsJsonFileName,
                "testStudentsJsonFileName": self.testStudentsJsonFileName}

    def createFilesFrom(self, brmOgrDersFileName: str, brmDersFileName: str, testPeriod: (int, int)):
        courseNameCreditDict = self.getCourseList(brmDersFileName)
        self.getStudentsObjects(brmOgrDersFileName, testPeriod, courseNameCreditDict)

    def getCourseList(self, brmDersFileName: str) -> dict:  # coursename, kredi
        # self.courseListCsvFileName deki dosyaya yazdırılıcak
        pass

    def getStudentsObjects(self, brmOgrDersFileName: str, testPeriod: (int, int), courseNameCreditDict: dict):
        sTrain = Students()
        sTest = Students()
        # sTrain.addSingleCourse(....)
        # trainStudentsJsonFileName testStudentsJsonFileName deki dosyalar yazdırılıcak
        sTrain.toJson(self.trainStudentsJsonFileName)
        sTest.toJson(self.testStudentsJsonFileName)
        pass

if __name__ == "__main__":
    import pprint
    FC = FileCreator()
    FC.createFilesFrom("resources/BrmOgrDers.xls", "resources/BrmDers.xls", (2018, 2))
    pprint.pprint(FC.getFileNames())
