from Test import Test

T = Test({'courseListCsvFileName': 'courseList.csv',
         'hiddenCsvFileName': 'hidden.csv',
         'observedCsvFileName': 'observed.csv',
         'testStudentsJsonFileName': 'testStudents.json',
         'trainStudentsJsonFileName': 'trainStudents.json'})

T.executeTest()
T.displayResults()