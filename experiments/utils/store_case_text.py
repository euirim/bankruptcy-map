from multiprocessing import Pool
import os

from case import Case

def store_doc_text(doc):
    url = doc.get_file_url()
    if not doc.is_available() and not url:
        return
    
    try:
        doc.download()
    except:
        print(f'({doc.get_id()}) ERROR: Cannot download text.')

    dest_fn = f'{dir}/{doc.get_id()}'

    if doc.text is None:
        print(f'({doc.get_id()}) ERROR: Downloaded text is empty.')
        return

    with open(dest_fn, 'w') as f:
        f.write(doc.text)

def store_case_text(case, dir):
    for entry in case.get_entries():
        for doc in entry.get_documents():
            store_doc_text(doc)

if __name__=='__main__':
    cases_dir = 'nysb_all_chap_11'
    cases_path = f'../data/{cases_dir}'
    dir = f'../data/results_{cases_dir}'

    # make directory if it doesn't exist
    try:
        os.stat(dir)
    except:
        os.makedirs(dir, exist_ok=True)

    def step(pair):
        i, file = pair
        if file.endswith(".json"):
            store_case_text(Case(os.path.join(cases_path, file)), dir)
            print(f'{file} processed (No. {i}).')

    with Pool(4) as p:
        p.map(step, list(enumerate(os.listdir(cases_path))))
