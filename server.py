import json
import random
from pathlib import Path
from re import search

from flask import Flask, redirect
from flask_restful import Api, Resource, abort

app = Flask(
    __name__,
    static_url_path='',
    static_folder='web/static',
    template_folder='web/templates'
)
api = Api(app)

# Utility functions


def get_absolute_path():
    """Gets the path of the code directory."""
    return str(Path(__file__).parent.absolute())


def fetch_word_data(file_path="data/word_data.json"):
    """Fetches the word data to be used by the API.

    :param file_path: A string, the path to the word data file from the project's directory.
    """

    file_path = get_absolute_path() + "/" + file_path

    with open(file_path, "r") as file_data:
        return json.loads(file_data.read())

# Data manipulation


def search_data(word, word_data):
    """Returns a dictionary built from a search through the word data.

    Searches are ranked as follows:
    * The found word is the user's word verbatim.
    * The found word begins with the user's word.
    * The word is a substring of the found word.
    * The found word has a definition equal to the user's word.
    * The found word has a substring equal to the user's word.

    :param word: A string, the word to search for.
    :param word_data: A dict, the word data to search through.
    """

    word = word.lower()

    matches = {
        "word_verbatim": [],
        "word_begins_with": [],
        "word_substring": [],
        "word_definition_verbatim": [],
        "word_definition_substring": [],
    }

    for word_info in word_data:
        word_name = word_info['word'].lower()

        word_definitions = []
        for word_type in list(word_info['definitions'].keys()):
            word_definitions.extend(word_info['definitions'][word_type])

        if word == word_name:
            matches['word_verbatim'].append({
                "word": word_name,
                "definitions": word_info['definitions'],
                "examples": word_info['examples'],
                "misc": word_info['misc'],
                "search_result_reason": "The word supplied is the word verbatim."
            })

        elif word_name.startswith(word):
            matches['word_begins_with'].append({
                "word": word_name,
                "definitions": word_info['definitions'],
                "examples": word_info['examples'],
                "misc": word_info['misc'],
                "search_result_reason": "The word starts with the word supplied."
            })

        elif search(word, word_name) != None:
            matches['word_substring'].append({
                "word": word_name,
                "definitions": word_info['definitions'],
                "examples": word_info['examples'],
                "misc": word_info['misc'],
                "search_result_reason": "The word supplied is a substring of the word."
            })

        elif word in word_definitions:
            matches['word_definition_verbatim'].append({
                "word": word_name,
                "definitions": word_info['definitions'],
                "examples": word_info['examples'],
                "misc": word_info['misc'],
                "search_result_reason": "The word supplied is a definition of the word."
            })

        elif set([search(word, definintion) for definintion in word_definitions]) != {None}:
            matches['word_definition_verbatim'].append({
                "word": word_name,
                "definitions": word_info['definitions'],
                "examples": word_info['examples'],
                "misc": word_info['misc'],
                "search_result_reason": "The word supplied is a substring of the definition."
            })

    return matches['word_verbatim'] + matches['word_begins_with'] + matches['word_substring'] + matches['word_definition_verbatim'] + matches['word_definition_substring']


# Resource definitions
class RawData(Resource):
    def get(self):
        """Returns the raw data the program uses as the source of information for the Toki Pona API."""
        return fetch_word_data()


class Word(Resource):
    def get(self, word):
        """Get information about a particular word, such as the definition and example usage.

        :param word: A string, the word to look up.
        """

        word_data = fetch_word_data()
        return search_data(word, word_data)


class Random(Resource):
    def get(self):
        """Gets a random word and returns it."""

        word_data = fetch_word_data()
        return random.choice(word_data)


# Add resources
api.add_resource(RawData, '/data')
api.add_resource(Word, '/word/<string:word>')
api.add_resource(Random, '/random')

# Add other routes


@app.route('/')
def index():
    return redirect('/index.html')


if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)
