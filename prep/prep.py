# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 21:15:59 2021

@author: ogulc
"""

import numpy as np
import pandas as pd
import json
from apyori import apriori
import pickle


events = json.load(open("events.json", encoding="UTF-8"))["events"]
events_df = pd.DataFrame(events)
events_df["price"] = pd.to_numeric(events_df["price"])
events_df["productid"] = events_df["productid"].astype(str)

events_df_grouped = events_df.groupby(["sessionid"]).agg({
    "price": np.sum,
    "productid": lambda s: list(s),

})

events_df_grouped = events_df_grouped.reset_index()

items = events_df_grouped["productid"]
items = list(items)

store_data = pd.DataFrame(items)

df_shape = store_data.shape
n_of_transactions = df_shape[0]
n_of_products = df_shape[1]
# Converting our dataframe into a list of lists for Apriori algorithm
records = []
for i in range(0, n_of_transactions):
    records.append([])
    for j in range(0, n_of_products):
        if str(store_data.values[i, j]) is not None:
            records[i].append(str(store_data.values[i, j]))
        else:
            continue

association_rules = apriori(records, min_support=0.0010, min_confidence=0.001)
association_results = list(association_rules)

merged = store_data[0]
for i in range(1, n_of_products):
    merged = merged.append(store_data[i])

ranking = merged.value_counts(ascending=False)
ranked_products = list(ranking.index)

lookup_table = {}

for item in association_results:
    pair = item[0]

    items = [x for x in pair]
    if len(items) < 10:

        items_to_append = items

        i = 0

        while len(items) < 10:

            if ranked_products[i] not in items:
                items_to_append.append(ranked_products[i])

            i += 1

    lookup_table[items_to_append[0]] = items_to_append[1:]

lookup_table['default_recommendation'] = ranked_products[:10]

pickle.dump(lookup_table, open("lookup_table.pickle", "wb"))
