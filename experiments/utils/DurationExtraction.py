import sys
import os
sys.path.append("..")
from utils.case import Case, DocketEntry, Document, Party

DATA_LOCATION = "../data/samples"

case_files = []
for file in os.listdir(DATA_LOCATION):
    if file.endswith(".json"):
        case_files.append(os.path.join(DATA_LOCATION, file))

#Returns duration of a case in days
def FindDurationFromCase(case):
    newest_date = ""
    entries = case.get_entries()
    if(len(entries) > 1):
        oldest_date = entries[0].get_date_filed()
        newest_date = entries[1].get_date_filed()
        for i in range(2, len(entries)):
            entry_date = entries[i].get_date_filed()
            if(entry_date > newest_date):
                newest_date = entry_date
        duration = newest_date - oldest_date
        return duration.days
    elif(len(entries) == 1):
        oldest_date = entries[0].get_date_filed()
        newest_date = entries[0].get_date_modified()
        duration = newest_date - oldest_date
        return duration.days
                         
    #In the case no duration is found, return None
    return None

#Example with a chapter 11 case:
FindDurationFromCase(Case("../data/samples_5000/7325782.json"))
