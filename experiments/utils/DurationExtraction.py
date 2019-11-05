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
def FindDurationAndStartDateFromCase(case):
    if(case.get_date_filed() != None and case.get_date_terminated().date() != datetime.datetime.utcnow().date()):
        duration = case.get_date_terminated() - case.get_date_filed()
        return [case.get_date_filed(), duration.days]
    #In the case no duration is found, return None
    return None

#Example with a chapter 11 case:
FindDurationFromCase(Case("../data/samples/7325782.json"))
