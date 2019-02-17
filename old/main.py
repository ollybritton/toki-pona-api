import json
import re

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


def get_word_json():
    with open("data/words.json", "r") as f:
        return json.dumps(json.loads(f.read()))


def get_word_dict():
    data = sorted(json.loads(get_word_json()), key=lambda x: x["word"])

    return data


def search(word):
    # Returns a search for a specific word.
    word_data = get_word_dict()

    matches = {
        "is_word": [],
        "word_begins_with": [],
        "in_word": [],
        "is_definition": [],
        "in_definition": []
    }

    for x in word_data:
        word_types = list(x["definitions"].keys())

        all_word_definitions = []

        for word_type in word_types:
            all_word_definitions.extend(
                x["definitions"][word_type]["meanings"])

        for i in range(len(all_word_definitions)):
            all_word_definitions[i] = re.sub(
                r'\(.+\)', '', all_word_definitions[i])

            all_word_definitions[i] = re.sub(
                r'[^a-z|^ ]', '', all_word_definitions[i])

        if x["word"] == word:
            x["misc"]["search_result_reason"] = "is_word"
            matches["is_word"].append(x)

            continue

        if x["word"].startswith(word):
            x["misc"]["search_result_reason"] = "word_begins_with"
            matches["word_begins_with"].append(x)

            continue

        if re.search(word, x["word"]) != None:
            x["misc"]["search_result_reason"] = "in_word"
            matches["in_word"].append(x)

            continue

        if word in all_word_definitions:
            x["misc"]["search_result_reason"] = "is_definition"
            matches["is_definition"].append(x)

            continue

        if re.search(word, " ".join(all_word_definitions)) != None and len(word) > 3:
            x["misc"]["search_result_reason"] = "in_definition"
            matches["in_definition"].append(x)

            continue

    return matches["is_word"] + matches["word_begins_with"] + matches["in_word"] + matches["is_definition"] + matches["in_definition"]


class Data(Resource):
    def get(self, data_name):
        # This resource will return the raw data that is used in the api.
        if data_name == "words":
            return get_word_dict()


class Search(Resource):
    def get(self, word):
        # This resource allows you to search for a specific word, and results are then organised in order of how likely each is.
        return search(word)


api.add_resource(Data, "/data/<data_name>")
api.add_resource(Search, "/search/<word>")

if __name__ == '__main__':
    app.run()
