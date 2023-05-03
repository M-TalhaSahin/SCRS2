import pandas as pd
import csv
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
        excel_data = pd.read_excel(brmDersFileName, dtype=str)  # Read Excel data
        # Get DERSKODU as unique key for courseList dictionary
        courseList_dict = {}
        with open("data/courseList.csv", mode="w", newline="", encoding='utf-8-sig') as dosya:
            yazici = csv.writer(dosya)
            yazici.writerow(['COURSENAME', 'KR', 'ZORSEC', 'TEMBIL', 'MESLEK', 'INSANB', 'TASARIM'])

            for index, row in excel_data.iterrows():
                lesson_code = row['DERS_KODU']
                # Get values for each DERSKODU key
                if lesson_code not in courseList_dict:
                    courseList_dict[lesson_code] = {
                        'ders_adi': row['DERSADI'],
                        'kr': row['KR'],
                        'zor_sec': row['ZORSEC'],
                        'tem_bil': row['TEMBIL'],
                        'meslek': row['MESLEK'],
                        'genel': row['INSANB'],
                        'tasarim': row['TASARIM']
                    }
                    yazici.writerow(
                        [lesson_code + " " + row['DERSADI'], row['KR'], row['ZORSEC'], row['TEMBIL'], row['MESLEK'],
                         row['INSANB'], row['TASARIM']])
            dosya.close()
        return courseList_dict  # return courseList as a dictionary

    def getStudentsObjects(self, brmOgrDersFileName: str, testPeriod: (int, int), courseNameCreditDict: dict):
        sTrain = Students()
        sTest = Students()
        excel_data = pd.read_excel(brmOgrDersFileName, dtype=str)  # Read Excel data
        for index, row in excel_data.iterrows():
            if((row['YIL'])==str(testPeriod[0]) and (row['DONEM'])==str(testPeriod[1]) ):
                ders_kodu = row['DERS_KODU']
                sTest.addSingleCourse(row['OGRNO'],row['DERS_KODU'],testPeriod,float(row['SAYISAL']),int(courseNameCreditDict[ders_kodu]['kr']))
            else:
                sTrain.addSingleCourse(row['OGRNO'],row['DERS_KODU'],testPeriod,float(row['SAYISAL']),int(courseNameCreditDict[row['DERS_KODU']]['kr']))
        sTrain.toJson(self.trainStudentsJsonFileName)
        sTest.toJson(self.testStudentsJsonFileName)

if __name__ == "__main__":
    import pprint
    FC = FileCreator()
    FC.createFilesFrom("resources/BrmOgrDers.xls", "resources/BrmDers.xls", (2018, 2))
    pprint.pprint(FC.getFileNames())
