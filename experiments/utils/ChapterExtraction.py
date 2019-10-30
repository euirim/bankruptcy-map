import sys
import os
sys.path.append("..")
from utils.case import Case, DocketEntry, Document, Party

DATA_LOCATION = "../data/samples_5000"

case_files = []
for file in os.listdir(DATA_LOCATION):
    if file.endswith(".json"):
        case_files.append(os.path.join(DATA_LOCATION, file))

#Returns chapter of a case based on the voluntary petition for that case
def FindChapterNumberFromCase(case):
    for entry in case.get_entries():
        descr = entry.get_description()
        if("petition" in descr.lower()):
            if("chapter 7" in descr.lower()):
                return 7
            elif("chapter 11" in descr.lower()):
                return 11
            elif("chapter 12" in descr.lower()):
                return 12
            elif("chapter 13" in descr.lower()):
                return 13
            elif("chapter 15" in descr.lower()):
                return 15
        else:
            for doc in entry.documents:
                doc_descr = doc.get_description()
                if("petition" in doc_descr.lower()):
                    if("chapter 7" in doc_descr.lower()):
                        return 7
                    elif("chapter 11" in doc_descr.lower()):
                        return 11
                    elif("chapter 12" in doc_descr.lower()):
                        return 12
                    elif("chapter 13" in doc_descr.lower()):
                        return 13
                    elif("chapter 15" in doc_descr.lower()):
                        return 15
                                
    #In the case no chapter is found, return None
    return None

#Example with a chapter 11 case
print(FindChapterNumberFromCase(Case("../data/samples_5000/7325782.json")))
