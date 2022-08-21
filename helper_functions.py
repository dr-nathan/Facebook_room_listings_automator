#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 22:25:41 2021

@author: nathanvaartjes
"""
import re
import pickle

# load pickles with all streetnames and buurt-/wijknames of Amsterdam
# is global, so it can be accessed from all functions
with open("streetnames_full.pickle", "rb") as f:
    streetnames_amsterdam = pickle.load(f)

with open("buurtnames_full.pickle", "rb") as f:
    buurten_en_wijken_amsterdam = pickle.load(f)


def cleanup(post):
    post_text = post["post_text"]
    lowered = post_text.lower()  # remove Uppercase
    text_with_dot = lowered.translate(
        str.maketrans("\n,", " .", "!\"#$%&'()*+/:;<=>?@[\\]^_`{|}~")
    )  # stripped of punctuation except . and ,
    text = text_with_dot.translate(str.maketrans("", "", ".-"))
    return (text, text_with_dot)


def only_girls(text):
    keywords = ["meiden", "girls", "vrouwelijke"]
    for i in keywords:
        if i in text:
            return True
    return False


def extract_location(post, text):
    postcode = None

    if post["listing_location"][0:4].isdigit():  # try to get postcode directly first
        postcode = int(post["listing_location"][0:4])  # return it if found

    streets = []
    buurts_en_wijken = []
    for word in text.split(" "):  # get all recognized street and buurt names
        if word in streetnames_amsterdam["Naam openbare ruimte"].values:
            streets.append(word)
        if word in buurten_en_wijken_amsterdam.values:  # if it matches a buurt, save it
            buurts_en_wijken.append(word)
    return (postcode, streets, buurts_en_wijken)


def extract_size(text, text_with_dot):
    if ("m2" or "m 2" or "vierkante" or "squared") in text_with_dot:  # first check if m2 is mentionned at all
        tries = ["m2", "m 2", "vierkante", "squared"]

        for i in tries:  # try for all 4 syntaxes

            # get all matches of current try
            ixes = [m.start() for m in re.finditer(i, text_with_dot)]

            for ix in ixes:
                numbers = [
                    x for x in text_with_dot[ix - 5: ix] if (x.isdigit() or x == '.')
                ]  # get all integers in 4 slots before target
                try:
                    size = float("".join(numbers))  # try to make float (should work)
                except ValueError:
                    # print(f'{i} didnt work, trying next version')
                    continue

                if 5.0 < size < 40.0:
                    return size
    return None


def check_tijdelijk(text):
    if ('tijdelijk' or 'onderhuur' or 'temporary' or 'verlenging') in text:
        return True
    return False


def location_evaluator(postcodes_of_interest, postcode, streets, buurts_en_wijken):

    # first, get all streets, and neighborhouds associated to postcode
    (postcodes_of_interest_str, streetnames_of_interest, buurten_of_interest, wijken_of_interest) =\
        get_streets_and_buurts_of_interest(postcodes_of_interest)

    if postcode != None:  # first check postcode
        if (
            postcode in postcodes_of_interest
        ):  # if postcode is a match, return success
            return True
        return False  # if it is no match, not an interesting location
    # if no postcodes found, try streetnames and buurts

    if streets != []:
        if all(street in streetnames_of_interest for street in streets):
            return True
        return False
    # if no streets found either, check buurten and wijken #TODO: wijken and buurten concatenated, a bit hard to read. Either keep separate or merge everywhere
    if buurts_en_wijken != []:
        if all(buurt in (buurten_of_interest or wijken_of_interest) for buurt in buurts_en_wijken):
            return True
        return False
    # if nothing is found
    return None


def get_streets_and_buurts_of_interest(postcodes_of_interest):
    """
    Function takes postcodes of interest and returns all associated streets, buurts and wijken

    Parameters
    ----------
    postcodes_of_interest : list
        List of postcodes in which the house should be situated.

    Returns
    -------
    streetnames_of_interest : list
        All streets in the specified postcodes.
    buurten_of_interest : list
        All buurten in the specified postcodes.
    wijken_of_interest : list
        All wijken in the specified postcodes.

    """

    postcodes_of_interest_str = [str(x) for x in postcodes_of_interest]  # convert to string

    streetnames_of_interest = []  # get relevant streetnames, based on postcode
    stadsdelen_of_interest = []
    GGW_of_interest = []
    buurten_of_interest = []
    wijken_of_interest = []

    for i, x in enumerate(streetnames_amsterdam.values):

        if x[1] in postcodes_of_interest_str:

            streetnames_of_interest.append(x[0])
            stadsdelen_of_interest.append(x[2])
            GGW_of_interest.append(x[3])
            wijken_of_interest.append(x[4])
            buurten_of_interest.append(x[5])

    streetnames_of_interest = set(streetnames_of_interest)
    stadsdelen_of_interest = set(stadsdelen_of_interest)
    GGW_of_interest = set(GGW_of_interest)
    buurten_of_interest = set(buurten_of_interest)
    wijken_of_interest = set(wijken_of_interest)

    return (postcodes_of_interest_str,
            streetnames_of_interest,
            buurten_of_interest,
            wijken_of_interest
            )
