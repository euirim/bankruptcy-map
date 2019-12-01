import logging
from multiprocessing import Pool, current_process
import multiprocessing_logging
import os

from case import Case
        

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%m-%d %H:%M',
    filename='../logs/total.log',
    filemode='a'
)
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(console_formatter)

total_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
errorsLog = logging.FileHandler(filename='../logs/errors.log', mode='a')
errorsLog.setLevel(logging.WARNING)
errorsLog.setFormatter(total_formatter)

logger = logging.getLogger('store_case_text')
logger.addHandler(console)
logger.addHandler(errorsLog)

multiprocessing_logging.install_mp_handler()


class DocDownloadFailed(Exception):
    pass


class DocDownloadEmpty(Exception):
    pass


class DocTextSaveFailed(Exception):
    pass


class CaseAPIFailed(Exception):
    pass


def store_doc_text(doc, case, entry, loc):
    url = doc.get_file_url()
    if not doc.is_available() and not url:
        return
    
    try:
        doc.download()
    except Exception as err:
        raise DocDownloadFailed(f'Document download failed. Error: {err}')
        return

    if doc.text is None:
        raise DocDownloadEmpty('Downloaded text is empty.')
        return

    dest_fn = f'{loc}/{case.get_id()}_{entry.get_id()}_{doc.get_id()}'

    try:
        with open(dest_fn, 'w') as f:
            f.write(doc.text)
    except:
        raise DocTextSaveFailed('Cannot write text to file.')


def store_case_text(case, dir, case_file, case_idx):
    for entry_idx, entry in enumerate(case.get_entries()):
        logger.debug(gen_log_message('Storing entry.', case_file, case_idx))

        total_docs = len(entry.get_documents())
        for doc_idx, doc in enumerate(entry.get_documents()):
            logger.debug(gen_log_message(f'Storing document {doc_idx}.', case_file, case_idx))

            try:
                store_doc_text(doc, case, entry, dir)
            except Exception as err:
                logger.error(gen_log_message(f'Failed to store text of doc {doc_idx}. Explanation: {err}', case_file, case_idx))
                continue

            logger.debug(gen_log_message(f'Finished storing document {doc_idx}.', case_file, case_idx))

        logger.debug(gen_log_message('Finished storing entry.', case_file, case_idx))


def gen_log_message(message, case_file, case_index):
    return f'(p: {current_process().name} | c: {case_file} | i: {case_index}) {message}'


if __name__=='__main__':
    cases_dir = 'nysb_all_chap_11'
    cases_path = f'../data/{cases_dir}'
    dir = f'../data/results_{cases_dir}'

    # make output directory if it doesn't exist
    try:
        os.stat(dir)
    except:
        os.makedirs(dir, exist_ok=True)

    # get total number of cases
    total_cases = len(os.listdir(cases_path))
    logger.info(f'Total number of cases: {total_cases}')

    def step(pair):
        idx, file = pair
        if file.endswith(".json"):
            try:
                logger.info(gen_log_message('Begin processing case.', file, idx))

                try:
                    case = Case(os.path.join(cases_path, file))
                except Exception as err:
                    raise CaseAPIFailed(f'{err}')

                store_case_text(case, dir, file, idx)
                
                logger.info(gen_log_message('Successfully processed case.', file, idx))
            except Exception as err:
                logger.error(
                    gen_log_message(
                        f'Processing case failed.\n Explanation: {err}', 
                        file, 
                        idx
                    )
                )

    num_cores = os.cpu_count()
    if num_cores is None:
        num_cores = 16        

    with Pool(num_cores) as p:
        p.map(step, list(enumerate(os.listdir(cases_path))), chunksize=10)
