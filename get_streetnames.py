#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 18:23:26 2021

@author: nathanvaartjes
"""
import pandas as pd
import time
import pickle

start = time.perf_counter()
straatnamen = pd.read_csv("130950b2-0563-4619-9726-b8046faf586b.csv", sep=";", dtype=str)

no_dup = straatnamen.drop_duplicates(subset="Naam openbare ruimte")

# keep only columns of interest
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


translator = str.maketrans('/', " ", '!"#$%&\'()*+,.:;<=>?@[\\]^_`{|}~')

final['Postcode'] = final['Postcode'].apply(lambda L: '0000' if isinstance(L, float) else L[0:4])
final['Naam gebiedsgerichtwerkengebied'] = final['Naam gebiedsgerichtwerkengebied'].\
    apply(lambda L: 'onbekend' if isinstance(L, float) else L.lower().translate(translator))
final["Naam openbare ruimte"] = final["Naam openbare ruimte"].\
    apply(lambda x: x.lower().translate(str.maketrans(translator)))
final["Naam stadsdeel"] = final["Naam stadsdeel"].\
    apply(lambda x: x.lower().translate(str.maketrans(translator)))
final["Naam Wijk"] = final["Naam Wijk"].\
    apply(lambda x: x.lower().translate(str.maketrans(translator)))
final["Naam buurt"] = final["Naam buurt"].\
    apply(lambda x: x.lower().translate(str.maketrans(translator)))
    

#overleg givea a bunch of false positives    
final= final[final['Naam openbare ruimte'] != 'overleg']

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
