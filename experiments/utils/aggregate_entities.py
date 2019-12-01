import sys
import os
import re
sys.path.append("..")

import spacy
nlp = spacy.load("en_core_web_lg")

from utils.case import Case, DocketEntry, Document, Party
DATA_LOCATION = "../data/results_nysb_all_chap_11" #CHANGE THIS TO REFLECT WHERE EXTRACT TXT FILES ARE

def find_repeat(s):
    tokens = s.split()
    if len(tokens) <= 1:
        return s
    if len(tokens) == 4:
        if tokens[0] == tokens[2] and tokens[1] == tokens[3]:
            return tokens[0]+" "+tokens[1]
    if len(tokens) == 6:
        if tokens[0] == tokens[3] and tokens[1] == tokens[4] and tokens[2] == tokens[5]:
            return tokens[0]+" "+tokens[1]+" "+tokens[2]
    return s

#aggregate orgs mentioned in file
remove_words = ['po box', 'el', 'signature'] #words to remove from an entity
def clean_org(orig):
    cleaned = orig.lower().strip()
    cleaned = re.sub('  ', ' ', cleaned)
    cleaned = re.sub('[^A-Za-z0-9 ]+', '', cleaned)
    cleaned = find_repeat(cleaned)

    no_spaces = re.sub(' +', '', cleaned)
    if (len(no_spaces) == 0):
        return ""
    #all the same letter (i.e. 'iii iii iii')
    if (no_spaces == len(no_spaces) * no_spaces[0]):
        return ""

    # remove remove_words from entity
    for word in remove_words:
        cleaned = re.sub(word, '', cleaned)

    tokens = cleaned.split()
    if len(tokens) <= 1:
        return ""
    if len(max(tokens, key=len)) <= 2: #no token longer than 2 characters
        return ""
    if tokens[0] == "the":
        return ""
    for token in tokens: #get rid of zip codes -> presume address
        if token.isdigit() and len(token) == 5:
            return ""

    #get rid of trailing whitespace
    cleaned = cleaned.rstrip()
    if cleaned.isdigit():
        return ""
    return cleaned

blacklist = ["court", "united states", 'debtors', 'social security', 'motion', "employer", "debtor",
             'form', 'docket', 'state of', 'agreement', 'floor', 'street', 'taxpayer', 'petition', "fee", "number"]

def most_freq_orgs(ents):
    orgs = {}
    for ent in ents:
        if ent.label_ == "ORG":
            org = clean_org(ent.text)
            #blacklist certain org words:
            for word in blacklist:
                if word in org:
                    org = ""
                    break
            if org == "":
                continue
            if org in orgs:
                orgs[org] += 1
            else:
                orgs[org] = 1
    return orgs

#aggregate people mentioned in file
remove_words_ppl = ["signature"]

def clean_name(orig):
    cleaned = orig.lower().strip()
    cleaned = re.sub('  ', ' ', cleaned)
    cleaned = re.sub('[^A-Za-z ]+', '', cleaned)

    tokens = cleaned.split()
    if (len(tokens) <= 1):
        return ""
    if len(max(tokens, key=len)) <= 2: #no token longer than 2 characters
        return ""

    # remove remove_words from entity
    for word in remove_words_ppl:
        cleaned = re.sub(word, '', cleaned)

    cleaned = find_repeat(cleaned)

    #all the same letter (i.e. 'iii iii iii')
    no_spaces = re.sub(' +', '', cleaned)
    if (no_spaces == len(no_spaces) * no_spaces[0]):
        return ""

    #get rid of trailing whitespace
    cleaned = cleaned.rstrip()
    return cleaned

blacklist_ppl = ["court", "clerk", "name of", "debtor", "united states"]

def most_freq_persons(ents):
    people = {}
    for ent in ents:
        if ent.label_ == "PERSON":
            person = clean_name(ent.text)
            #blacklist certain org words:
            for word in blacklist_ppl:
                if word in person:
                    person = ""
                    break
            if person == "":
                continue
            if person in people:
                people[person] += 1
            else:
                people[person] = 1
    return people

# move potential non-people in ppl to org
company_indicator = ["inc", "llc", "llp", "corp"]

#adds name, count to dict
def add_to_dict(d, name, count):
    if name in d:
        d[name] = d[name] + count
    else:
        d[name] = count
    return d

#move things that are actually orgs from ppl to orgs
def move_ppl_to_orgs(orgs,ppl):
    to_delete = []
    for person, count in ppl.items():
        tokens = person.split()
        if tokens[-1] in company_indicator:
            orgs = add_to_dict(orgs,person,count)
            to_delete.append(person)
    for delete in to_delete:
        del ppl[delete]
    return orgs, ppl

def print_top_3(A):
    top_keys = sorted(A, key=A.get, reverse=True)[:3]
    for key in top_keys:
        print (A[key],key)

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

#returns if it's close (bool), string before, string after (one will become the other)
def close_enough(s1,s2):
    dist = levenshteinDistance(s1,s2)
    #one contained in another
    if s1 in s2 and dist < 8:
        return True, s2, s1
    if s2 in s1 and dist < 8:
        return True, s1, s2
    #edit distance is small
    if dist < 3:
        return True, s1, s2 #this is an arbitrary choice
    return False, None, None

#combines similar entities
def agg_dict(A):
    combined = {} # before:after

    for s1 in A.keys():
        for s2 in A.keys():
            if s1 == s2:
                continue
            is_close, before, after = close_enough(s1,s2)
            if s1 == after:
                continue
            if is_close:
                # make sure not a loop
                if after not in combined or combined[after] != before:
                    combined[before] = after
                    print(before,"->", after)

    to_delete = []
    for before, after in combined.items():
        item = after
        count = A[before]
        A = add_to_dict(A, item, count)
        to_delete.append(before)
    for delete in to_delete:
        del A[delete]
    return A

# EXAMPLE USAGE:
# # EXTRACT ORGS AND PPL INTO MAPS
# file_to_orgs = {} # maps file name to a map of orgs + counts
# file_to_ppl = {} # maps file name to a map of people + counts
#
# for file in os.listdir(DATA_LOCATION):
#     doc = nlp(open(os.path.join(DATA_LOCATION, file)).read())
#     orgs = most_freq_orgs(doc.ents)
#     ppl = most_freq_persons(doc.ents)
#     orgs, ppl = move_ppl_to_orgs(orgs, ppl)
#     orgs = agg_dict(orgs)
#     ppl = agg_dict(ppl)
#     print(file)
#     print("ORGS:", orgs)
#     print("PPL:", ppl)
#     print("\n")
#     file_to_ppl[file] = ppl
#     file_to_orgs[file] = orgs

# returns a map of people+counts for multiple files
# parameter: array of strings of file names
def mult_files_ppl(files):
    if len(files) == 0 or files[0] not in file_to_ppl:
        return None
    starting_set = file_to_ppl[files[0]]
    for index in range(1,len(files)):
        curr_ppl = file_to_ppl[files[index]]
        # add this files' items to starting_set
        for name, count in curr_ppl.items():
            if name in starting_set:
                starting_set[name] = starting_set[name] + count
            else:
                starting_set[name] = count
    return starting_set
