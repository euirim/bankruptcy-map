import sys
import string
import nltk
from utils.case import Case, DocketEntry, Document, Party
import os

class CoherenceDetector:
    def __init__(self):
        self.english_vocab = set(w.lower() for w in nltk.corpus.words.words())
        self.english_vocab.add(w.lower() for w in nltk.corpus.brown.words())

    # Checks coherence of text based on number of real words.
    # If empty text is passed in, returns None
    def check_coherence(self, text):
        if text is None:
            return
        num_coherent = 0
        words = text.split()
        for word in words:
            cleaned_word = word.translate(str.maketrans('', '', string.punctuation))
            if cleaned_word.lower() in self.english_vocab:
                num_coherent += 1
        if (num_coherent/len(words)) < 0.65:
            return False
        else:
            return True

# Example Usage:
# detector = CoherenceDetector()
# sys.path.append("..")
# DATA_LOCATION = "../data/samples_5000"
# case_files = []
# num_coherent = 0
# num_bad = 0
# for file in os.listdir(DATA_LOCATION):
#     if file.endswith(".json"):
#         case_files.append(os.path.join(DATA_LOCATION, file))
# for file in case_files:
#     case = Case(file)
#     for entry in case.get_entries():
#         for doc in entry.documents:
#             doc.download()
#             coherent = detector.check_coherence(doc.text)
#             if coherent is not None:
#                 if coherent:
#                     num_coherent += 1
#                 else:
#                     num_bad += 1
# print(num_coherent)
# print(num_bad)
