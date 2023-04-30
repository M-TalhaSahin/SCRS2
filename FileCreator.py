import pandas as pd


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
        pass


if __name__ == "__main__":
    import pprint
    FC = FileCreator()
    FC.createFilesFrom("resources/BrmOgrDers.xls", "resources/BrmDers.xls", (2018, 1))
    pprint.pprint(FC.getFileNames())
