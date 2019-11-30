import json
import os
import urllib.request
import shutil

import arrow
from pdf2image import convert_from_path
import pytesseract
from PIL import Image


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
            return arrow.get(self.__data["date_terminated"]).date()
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

            if descr is not None and "petition" in descr.lower():
                if "chapter 7" in descr.lower():
                    return 7
                elif "chapter 11" in descr.lower():
                    return 11
                elif "chapter 12" in descr.lower():
                    return 12
                elif "chapter 13" in descr.lower():
                    return 13
                elif "chapter 15" in descr.lower():
                    return 15
            else:
                for doc in entry.documents:
                    doc_descr = doc.get_description()
                    if doc_descr is None or "petition" not in doc_descr.lower():
                        return None

                    if "chapter 7" in doc_descr.lower():
                        return 7
                    elif "chapter 11" in doc_descr.lower():
                        return 11
                    elif "chapter 12" in doc_descr.lower():
                        return 12
                    elif "chapter 13" in doc_descr.lower():
                        return 13
                    elif "chapter 15" in doc_descr.lower():
                        return 15
                                    
        return None


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
        url = self.get_file_url()
        if not self.is_available() and not url:
            return
        directory = 'tmp/{}'.format(self.get_id())

        # make directory if it doesn't exist
        try:
            os.stat(directory)
        except:
            os.makedirs(directory, exist_ok=True)

        pdf_filename = '{0}/doc.pdf'.format(directory)

        with urllib.request.urlopen(url) as response, open(pdf_filename, 'wb+') as out_file:
            response = response.read()
            out_file.write(response)

        # convert PDF to images
        page_images = convert_from_path(pdf_filename, dpi=300, thread_count=1, fmt='jpg')

        page_filenames = []
        # crop images
        for i, page in enumerate(page_images):
            page = page.crop(
                (
                    0, 
                    0 + page.height * 0.055, 
                    page.width, 
                    page.height - page.height * 0.11,
                )
            )
            fn = 'pg_{}.jpg'.format(i)
            fn = '{0}/{1}'.format(directory, fn)
            page.save(fn)
            page_filenames.append(fn)
        
        # convert images to text and compile
        texts = []
        tesseract_config = r'-l eng --oem 1'
        for fn in page_filenames:
            text = str(
                pytesseract.image_to_string(
                    Image.open(fn), config=tesseract_config
                )
            )
            text = text.replace('-\n', '')
            text = text.replace('\n', ' ')
            text = text.strip()
            texts.append(text)
            
        result = ' '.join(texts)
        self.text = result
        
        # clean up
        for fn in page_filenames:
            os.remove(fn)
        os.remove(pdf_filename)


class Party:
    def __init__(self, data):
        self.__data = data

    def get_id(self):
        return self.__data["id"]

    def get_name(self):
        return self.__data["name"]
