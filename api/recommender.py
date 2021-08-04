import pickle
import json

metadata = json.load(open("prep/meta.json", encoding="UTF-8"))["meta"]


def get_item_name(productid):
    try:
        return next(item for item in metadata if item["productid"] == productid)["name"]
    except StopIteration:
        pass


class Recommender:

    def __init__(self):
        lookup_table = "prep/lookup_table.pickle"
        with open(lookup_table, "rb") as f:
            self.lookup_table = pickle.load(f)

    def recommend(self, item):
        try:
            rec = self.lookup_table[item]
        except KeyError:
            rec = self.lookup_table["default_recommendation"]

        return {

            "recommendation": [get_item_name(r) for r in rec]
        }
