import os

from django.core.management.base import BaseCommand, CommandError
from utils.case import CaseObj, DocketEntryObj, DocumentObj
from bankruptcy.cases.models import Case, DocketEntry, Document


DATA_LOCATION = 'data/samples'

def find_chapter_number_from_case(case):
    for entry in case.get_entries():
        if not entry.get_description():
            continue 
        descr = entry.get_description().lower()
        if("voluntary petition" in descr):
            if("chapter 7" in descr):
                return 7
            elif("chapter 11" in descr):
                return 11
            elif("chapter 12" in descr):
                return 12
            elif("chapter 13" in descr):
                return 13
            elif("chapter 15" in descr):
                return 15
        
    return None


class Command(BaseCommand):
    help = 'Loads case data from JSON files into database.'

    def handle(self, *args, **options):
        self.stdout.write('Loading case data into the database...')
        case_files = []
        for file in os.listdir(DATA_LOCATION):
            if file.endswith('.json'):
                case_files.append(os.path.join(DATA_LOCATION, file))

        num_cases = len(case_files)
        num_loaded = 0
        num_failed = 0
        for case_num, fn in enumerate(case_files):
            try:
                case = CaseObj(fn)

                case_args = {
                    'name': case.get_case_name(),
                    'recap_id': case.get_id(),
                    'pacer_id': case.get_pacer_id(),
                    'date_filed': case.get_date_filed(),
                    'date_terminated': case.get_date_terminated(),
                    'date_blocked': case.get_date_blocked(),
                    'jurisdiction': case.get_jurisdiction(),
                    'chapter': find_chapter_number_from_case(case),
                    'data': case.get_raw_data(),
                }
                caseModelObject = Case.objects.create(**case_args)

                for entry in case.get_entries():
                    entry_args = {
                        'recap_id': entry.get_id(),
                        'date_filed': entry.get_date_filed(),
                        'description': entry.get_description(),
                        'case': caseModelObject,
                    }
                    entryModelObject = DocketEntry.objects.create(**entry_args)

                    for doc in entry.documents:
                        doc.download()
                        doc_args = {
                            'recap_id': doc.get_id(),
                            'pacer_id': doc.get_pacer_id(),
                            'doc_type': doc.get_type(),
                            'is_sealed': doc.is_sealed(),
                            'is_available': doc.is_available(),
                            'file_url': doc.get_file_url(),
                            'description': doc.get_description(),
                            'text': doc.text,
                            'docket_entry': entryModelObject,
                        }
                        Document.objects.create(**doc_args)

                self.stdout.write('Case {0} / {1} Loaded.'.format(case_num, num_cases))
                num_loaded += 1
            except:
                self.stdout.write('Case {0} / {1} Failed.'.format(case_num, num_cases))
                num_failed += 1
                
        self.stdout.write(
            self.style.SUCCESS(
                'Cases Loaded: {0}  |  Cases Failed: {1}'.format(num_loaded, num_failed)
            )
        )