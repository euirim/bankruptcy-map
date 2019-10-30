import json
import os
import urllib.request
import shutil

import PyPDF2
import arrow
import textract


class Case:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.__data = json.load(f)
        self.entries = []
        for entry_data in self.__data["docket_entries"]:
            entry = DocketEntry(entry_data)
            self.entries.append(entry)

    def get_raw_data(self):
        return self.__data

    def get_id(self):
        return self.__data["id"]

    def get_jurisdiction(self):
        return self.__data["court"]

    def get_date_filed(self):
        return arrow.get(self.__data["date_filed"])

    def get_date_terminated(self):
        return arrow.get(self.__data["date_terminated"])

    def get_date_blocked(self):
        return arrow.get(self.__data["date_blocked"])

    def get_pacer_id(self):
        return self.__data["pacer_id"]

    def get_case_name(self):
        return self.__data["case_name"]

    def get_entries(self):
        return self.entries


class DocketEntry:
    def __init__(self, data):
        self.__data = data
        self.documents = []
        for doc_data in self.__data["recap_documents"]:
            doc = Document(doc_data)
            self.documents.append(doc)
    
    def get_id(self):
        return self.__data["id"]

    def get_date_filed(self):
        return arrow.get(self.__data["date_filed"])

    def get_date_modified(self):
        return arrow.get(self.__data["date_modified"])

    def get_description(self):
        return self.__data["description"]

    def get_documents(self):
        return self.documents


class Document:
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
        return self.__data["description"]

    def is_sealed(self):
        return self.__data["is_sealed"]

    def is_available(self):
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


class Party:
    def __init__(self, data):
        self.__data = data

    def get_id(self):
        return self.__data["id"]

    def get_name(self):
        return self.__data["name"]
