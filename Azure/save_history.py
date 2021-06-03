import datetime
import pathlib
import time
import mysql.connector
import re

indexFilePath = pathlib.Path('/var/www/html/index.html')
MAX_RECORDS = 960

def check_if_modified(savedTimestamp):
    assert indexFilePath.exists(), f'No such file: {indexFilePath}'  # check that the file exists
    currentTimestamp = datetime.datetime.fromtimestamp(indexFilePath.stat().st_mtime)
    if (savedTimestamp == None):
        savedTimestamp = currentTimestamp
        modified = False
    elif (savedTimestamp == currentTimestamp):
        modified = False
    else:
        savedTimestamp = currentTimestamp
        modified = True
    return savedTimestamp, modified

def save_to_database():
    historyDatabase = mysql.connector.connect(
      host="localhost",
      user="swawproject",
      password="swawProject1324",
      database="SWaWProject"
    )
    index_len = 0
    while(index_len != 5):
        with open('/var/www/html/index.html', 'r') as reader:
            read_txt_index = reader.readlines()
            index_len = len(read_txt_index)
            if(index_len != 5):
                time.sleep(5)
    m = []
    for x in range(len(read_txt_index)):
        m.append(re.search('(?<=>).*?(?=<)', read_txt_index[x]))
    historyCursor = historyDatabase.cursor(buffered=True)

    historyCursor.execute("SELECT * FROM SWaWProject;")
    fetchResult = historyCursor.fetchall()
    if (len(fetchResult) >= MAX_RECORDS):
        historyCursor.execute("DELETE FROM SWaWProject ORDER BY ID LIMIT 1;")
    historyCursor.execute(f"INSERT INTO SWaWProject (date, temperature, humidity, pressure, illuminance) VALUES ('{m[0].group(0)}', {m[1].group(0)}, {m[2].group(0)}, {m[3].group(0)}, {m[4].group(0)});")
    historyDatabase.commit()
    historyCursor.close()
    historyDatabase.close()
if __name__ == "__main__":
    savedTimestamp = None
    while(1):
        time.sleep(5)
        savedTimestamp, modified = check_if_modified(savedTimestamp)
        if(modified == True):
            save_to_database()