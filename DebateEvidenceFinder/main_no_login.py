from python_backend.constants import PYTHON_BACKEND_FOLDER
from python_backend.python_backend_main import sift_cards, compile_cards, create_id_lst, create_id_dict, add_card_to_document, TEMPORARY_SEND_DOWNLOAD_FILES_FOLDER
from flask import Flask, request, render_template, send_from_directory
from docx import Document
import os

# TODO find the most common cards
# TODO from url note school, student, side, and tournament

SEARCH_MESSAGE = "Search Cards"

QUERY_KEY = 'query'

app = Flask(__name__)

compiled_cards = []
card_database_dict = {}
case_database_lst = {}

def add_temporary_send_file_path(filename):
    return f"{PYTHON_BACKEND_FOLDER}/{TEMPORARY_SEND_DOWNLOAD_FILES_FOLDER}/{filename}"

def temporary_send_download_files_folder():
    return f"{PYTHON_BACKEND_FOLDER}/{TEMPORARY_SEND_DOWNLOAD_FILES_FOLDER}"

def create_send_download_folder():
    try:
        os.makedirs(temporary_send_download_files_folder())
    except FileExistsError:
        print(f"Skipping Creating Folder \"{temporary_send_download_files_folder()}\" -- already exists")

def send_download(filename):
    return send_from_directory(temporary_send_download_files_folder(), path=filename, as_attachment=True)

def update_cards():
    global card_database_dict, card_database_lst
    compiled_cards = compile_cards(download=False, download_delay=6, download_all_versions=False)
    card_database_dict = create_id_dict(compiled_cards) # {id: <card_object>}
    card_database_lst = create_id_lst(compiled_cards) # (id, <card_object>)

@app.route("/", methods=['GET'])
def home():
    args = request.args
    if QUERY_KEY in args:
        query = args[QUERY_KEY]
        sifted_cards = sift_cards(query, True, cards=card_database_lst) # (id, (score, <card_object>))
        return render_template("home.html", placeholder=query, cards=sifted_cards, query=query, has_query=True)
    else:
        return render_template("home.html", placeholder=SEARCH_MESSAGE, has_query=False)

@app.route("/cards/<card_id>")
def card(card_id):
    card_id = int(card_id)
    args = request.args
    return render_template("card.html", card=card_database_dict[card_id], id=card_id, query=(args[QUERY_KEY] if QUERY_KEY in args else ""))

@app.route("/download/<card_id>", methods=['GET'])
def download(card_id):
    card_id = int(card_id)
    card = card_database_dict[card_id]
    document = Document()
    add_card_to_document(card, document)
    document.save(add_temporary_send_file_path(card.formatted_tag_as_filename))
    return send_download(card.formatted_tag_as_filename)

if __name__ == "__main__":
    create_send_download_folder()
    update_cards()
    app.run(host="0.0.0.0", port=80) # TODO update cards and clear the temporary downloads folder