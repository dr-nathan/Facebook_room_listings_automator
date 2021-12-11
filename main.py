import pickle
from facebook_scraper import get_posts
from helper_functions import (
    extract_location,
    extract_size,
    cleanup,
    only_girls,
    location_evaluator,
)


def run():
    matches = []
    # scrape FB
    posts = []
    for post in get_posts(
        group=712266335452208,
        pages=2,
        cookies='cookies.json',
        ):  # cookies='cookies.json'):
        posts.append(post)

    # TODO: check op tijdelijke kamers: tijdelijk, onderhuur, t/m., verlenging

    # analyze posts
    for i, post in enumerate(posts):
        if (
            not "listing_location" in post.keys()
        ):  # if not a listing, continue to next post
            continue
        onlygirls = False
        if i == 0:
            continue  # first post is weird so it doesnt have a listing price
        (text, text_with_dot) = cleanup(
            post
        )  # get post_text, remove uppercase and punctuation. One version with ., and one without
        if only_girls(text):
            onlygirls = True
            continue  # go to next post if ad is only for girls
        size = extract_size(
            text, text_with_dot
        )  # TODO: sometimes, size is with dot. ex, 11.5m2. Should take care of that.
        (postcode, streets, buurts) = extract_location(post, text)
        price = post["listing_price"][1:]

        print(
            f"""post {i}: size:{size}, only_girls:{onlygirls}, price:{price}, 
            location:{postcode, streets, buurts} \n"""
        )

        # analyze location
        success = location_evaluator(postcode, streets, buurts)

        if (
            size != None
            and size > 14
            and price != None
            and float(price) < 700
            and success != None
            and success
        ):
            print("hurray! found a match")
            matches.append(i)

    with open("matches.pickle", "wb") as f:
        pickle.dump(matches, f)
    # send_post_to_email(post)
