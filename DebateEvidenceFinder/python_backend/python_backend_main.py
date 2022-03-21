from os import write
from re import match
from python_backend.card import Card
from python_backend.scrape import download_cases, name_file, get_case_count
from python_backend.extract_cards import extract_cards, unique_cards
from python_backend.write_cards import write_cards, add_card_to_document
from python_backend.constants import *
from python_backend.similarity_search import find_top_similarity

def create_id_lst(lst):
    id_created = []
    for i, item in enumerate(lst):
        id_created.append((i, item))
    return id_created

def create_id_dict(lst):
    id_created = {}
    for i, item in enumerate(lst):
        id_created[i] = item
    return id_created

def compile_cards(download=False, download_delay=0, write_to_output_file=False, download_all_versions=False):
    if download:
        case_filenames = download_cases(download_delay=download_delay, download_all_versions=download_all_versions)
    else:
        case_filenames = [name_file(_) for _ in range(get_case_count())]

    all_cards = []

    for case_filename in case_filenames:
        dict_cards = extract_cards(case_filename)
        case_cards = [Card(tup[0], tup[1], tup[2]) for tup in dict_cards]
        all_cards += case_cards

    all_cards = unique_cards(all_cards)

    if write_to_output_file:
        write_cards(all_cards, f"{OUTPUT_FILES_FOLDER}/all_cards.docx")

    return all_cards

def sift_cards(query, has_id, cards=None, download=False, download_delay=0, write_to_output_file=False, download_all_versions=False): # (id, <card_object>)/<card_object>
    if cards is not None:
        all_cards = cards
    else:
        all_cards = compile_cards(download=download, download_delay=download_delay, write_to_output_file=write_to_output_file, download_all_versions=download_all_versions)

    matching_cards = find_top_similarity(query, all_cards, has_id) # (id, (score, <card_object>))/(score, <card_object>)

    return matching_cards