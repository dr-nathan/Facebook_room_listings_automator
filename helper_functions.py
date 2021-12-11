#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 22:25:41 2021

@author: nathanvaartjes
"""

import pickle

# import pickles with streetnames and buurtnames
with open("streetnames_full.pickle", "rb") as f:
    streetnames_amsterdam = pickle.load(f)

with open("buurtnames_full.pickle", "rb") as f:
    buurten_amsterdam = pickle.load(f)

# set params
postcodes_of_interest = [
    1011,
    1012,
    1013,
    1014,
    1015,
    1016,
    1017,
    1018,
    1019,
    1051,
    1052,
    1053,
    1054,
    1055,
    1056,
    1057,
    1058,
    1059,
    1071,
    1072,
    1073,
    1074,
    1075,
    1076,
    1077,
    1078,
    1079,
    1091,
    1092,
    1093,
    1094,
    1095,
    1096,
    1097,
    1098,
    1099,
]

postcodes_of_interest_str = [str(x) for x in postcodes_of_interest]  # convert to string

streetnames_of_interest = []  # get relevant streetnames, based on postcode
for i, x in enumerate(streetnames_amsterdam.values):
    if x[1] in postcodes_of_interest_str:
        streetnames_of_interest.append(x[0])
streetnames_of_interest = set(streetnames_of_interest)

buurten_of_interest = []  # get relevant buurtnames, based on postcode
for i, x in enumerate(streetnames_amsterdam.values):
    if x[1] in postcodes_of_interest_str:
        buurten_of_interest.append(x[3])
buurten_of_interest = set(buurten_of_interest)

wijken_of_interest = []
for i, x in enumerate(
    streetnames_amsterdam.values
):  # get relevant wijken, based on postcode
    if x[1] in postcodes_of_interest_str:
        wijken_of_interest.append(x[4])
wijken_of_interest = set(wijken_of_interest)


def cleanup(post):
    post_text = post["post_text"]
    lowered = post_text.lower()  # remove Uppercase
    text_with_dot = lowered.translate(
        str.maketrans("\n,", " .", "!\"#$%&'()*+-/:;<=>?@[\\]^_`{|}~")
    )  # stripped of punctuation except . and ,
    text = text_with_dot.translate(str.maketrans("", "", "."))
    return (text, text_with_dot)


def only_girls(text):
    keywords = ["meiden", "girls", "vrouwelijke"]
    for i in keywords:
        if i in text:
            return True
    return False


def extract_location(post, text):
    postcode = None
    try_postcode = post["listing_location"][
        0:4
    ].isdigit()  # first, try to extract postcode
    if try_postcode:
        postcode = int(post["listing_location"][0:4])  # return it if found

    streets = []
    buurts = []
    for word in text.split(" "):  # get all recognized street and buurt names
        if word in streetnames_amsterdam["Naam openbare ruimte"].values:
            streets.append(word)
        if word in buurten_amsterdam.values:  # if it matches a buurt, save it
            buurts.append(word)
    return (postcode, streets, buurts)


def extract_size(text, text_with_dot_comma):
    if (
        "m2" in text or "m 2" in text or "vierkante" in text or "squared" in text
    ):  # first check if m2 is mentionned at all
        tries = ["m2", "m 2", "vierkante", "squared"]
        for i in tries:  # try for all 4 syntaxes
            numbers = [
                x for x in text[text.find(i) - 5 : text.find(i)] if x.isdigit()
            ]  # get all integers in 4 slots before target
            try:
                size = float("".join(numbers))  # try to make float (should work)
            except ValueError:
                # print(f'{i} didnt work, trying next version')
                continue
            if 5 < size > 40 :
                return size

    else:
        return None


def location_evaluator(postcode, streets, buurts):
    if postcode != None:  # first check postcode
        if (
            postcode in postcodes_of_interest_str
        ):  # if postcode is a match, return success
            return True
        return False  # if it is no match, not an interesting location
    # if no postcodes found, try streetnames and buurts
    if streets != []:
        if all(street in streetnames_of_interest for street in streets):
            return True
        return False
    # if no streets found either, check buurten and wijken
    if buurts != []:
        if all(buurt in buurten_of_interest for buurt in buurts):
            return True
        return False
    # if nothing is found
    return None
