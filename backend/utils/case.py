import json
import os
import urllib.request
import shutil

import PyPDF2
import arrow


class CaseObj:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.__data = json.load(f)
        self.entries = []
        for entry_data in self.__data["docket_entries"]:
            entry = DocketEntryObj(entry_data)
            self.entries.append(entry)

    def get_raw_data(self):
        return self.__data

    def get_id(self):
        return self.__data["id"]

    def get_jurisdiction(self):
        return self.__data["court"]

    def get_date_filed(self):
        if self.__data["date_filed"]:
            return arrow.get(self.__data["date_filed"]).date()
        else:
            return None
        
    def get_date_created(self):
        if self.__data["date_created"]:
            return arrow.get(self.__data["date_created"]).date()
        else:
            return None

    def get_date_terminated(self):
        if self.__data["date_terminated"]:
            return arrow.get(self.__data["date_created"]).date()
        else:
            return None

    def get_date_blocked(self):
        if self.__data["date_blocked"]:
            return arrow.get(self.__data["date_blocked"]).date()
        else:
            return None

    def get_pacer_id(self):
        return self.__data["pacer_case_id"]

    def get_case_name(self):
        return self.__data["case_name"]

    def get_entries(self):
        return self.entries

    def get_chapter(self):
        """
        In most cases, extracts a chapter number
        purely from case metadata.
        """
        for entry in self.get_entries():
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


class DocketEntryObj:
    def __init__(self, data):
        self.__data = data
        self.documents = []
        for doc_data in self.__data["recap_documents"]:
            doc = DocumentObj(doc_data)
            self.documents.append(doc)
    
    def get_id(self):
        return self.__data["id"]

    def get_date_filed(self):
        if self.__data["date_filed"]:
            return arrow.get(self.__data["date_filed"]).date()
        else:
            return None

    def get_date_created(self):
        if self.__data["date_created"]:
            return arrow.get(self.__data["date_created"]).date()
        else:
            return None

    def get_description(self):
        if self.__data["description"]:
            return self.__data["description"].strip()
        else:
            return None

    def get_documents(self):
        return self.documents


class DocumentObj:
    def __init__(self, data):
        self.__data = data
        self.text = None
    
    def get_id(self):
        return self.__data["id"]
    
    def get_pacer_id(self):
        return self.__data["pacer_doc_id"]

    def get_type(self):
        return self.__data["document_type"]

    def get_description(self):
        if self.__data["description"]:
            return self.__data["description"].strip()
        else:
            return None

    def get_file_url(self):
        return self.__data["filepath_ia"]

    def is_sealed(self):
        if not self.__data["is_sealed"]:
            return False
        else:
            return self.__data["is_sealed"]

    def is_available(self):
        if not self.__data["is_available"]:
            return False
        else:
            return self.__data["is_available"]

    def download(self):
        url = self.__data["filepath_ia"]
        if not self.is_available() or not url:
            return
        directory = 'tmp'

        # make directory if it doesn't exist
        try:
            os.stat(directory)
        except:
            os.mkdir(directory)

        filename = '{0}/{1}'.format(directory, self.get_id())

        with urllib.request.urlopen(url) as response, open(filename, 'wb+') as out_file:
            response = response.read()
            out_file.write(response)

        with open(filename, 'rb') as f:
            pdfReader = PyPDF2.PdfFileReader(f)
            self.text = ''
            for page in pdfReader.pages:
                self.text += ' ' + page.extractText() 

            self.text = self.text.strip()

        # delete downloaded pdf
        os.remove(filename)


class PartyObj:
    def __init__(self, data):
        self.__data = data

    def get_id(self):
        return self.__data["id"]

    def get_name(self):
        return self.__data["name"]