#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 18:23:26 2021

@author: nathanvaartjes
"""
import pandas as pd
import time
import pickle
import string

start = time.perf_counter()
straatnamen = pd.read_csv("130950b2-0563-4619-9726-b8046faf586b.csv", sep=";")

no_dup = straatnamen.drop_duplicates(subset="Naam openbare ruimte")

final = no_dup[
    [
        "Naam openbare ruimte",
        "Postcode",
        "Naam stadsdeel",
        "Naam gebiedsgerichtwerkengebied",
        "Naam Wijk",
        "Naam buurt",
    ]
]


for i in range(len(final)):
    if isinstance(final.iloc[i]["Postcode"], float):  # means its a NaN.
        final.iloc[i]["Postcode"] = 0000
    else:
        final.iloc[i]["Postcode"] = final.iloc[i]["Postcode"][0:4]
    final.iloc[i]["Naam openbare ruimte"] = (
        final.iloc[i]["Naam openbare ruimte"]
        .lower()
        .translate(str.maketrans("", "", string.punctuation))
    )
    final.iloc[i]["Naam stadsdeel"] = (
        final.iloc[i]["Naam stadsdeel"]
        .lower()
        .translate(str.maketrans("", "", string.punctuation))
    )
    if isinstance(final.iloc[i]["Naam gebiedsgerichtwerkengebied"], float):
        final.iloc[i]["Naam gebiedsgerichtwerkengebied"] = "onbekend"
    else:
        final.iloc[i]["Naam gebiedsgerichtwerkengebied"] = (
            final.iloc[i]["Naam gebiedsgerichtwerkengebied"]
            .lower()
            .translate(str.maketrans("", "", string.punctuation))
        )
    final.iloc[i]["Naam Wijk"] = (
        final.iloc[i]["Naam Wijk"]
        .lower()
        .translate(str.maketrans("", "", string.punctuation))
    )
    final.iloc[i]["Naam buurt"] = (
        final.iloc[i]["Naam buurt"]
        .lower()
        .translate(str.maketrans("", "", string.punctuation))
    )
stop = time.perf_counter()

print(f"time:{stop-start}")


df = [
    final["Naam stadsdeel"],
    final["Naam gebiedsgerichtwerkengebied"],
    final["Naam Wijk"],
    final["Naam buurt"],
]  # put all wijk, buurt en gebieden together
buurten_uniek = pd.concat(df).drop_duplicates()


with open("streetnames_full.pickle", "wb") as f:
    pickle.dump(final, f)

with open("buurtnames_full.pickle", "wb") as f:
    pickle.dump(buurten_uniek, f)
