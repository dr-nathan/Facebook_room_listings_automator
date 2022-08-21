import pickle
from requests.exceptions import ConnectionError
from facebook_scraper import get_posts
from helper_functions import (
    extract_location,
    extract_size,
    check_tijdelijk,
    cleanup,
    only_girls,
    location_evaluator,
)


def run(max_price, min_size, postcodes_of_interest):
    matches = []

    # scrape FB

    # try max 5 times
    for i in range(5):
        posts = []
        try:
            for post in get_posts(
                group=712266335452208, pages=2, cookies="cookies.json",
            ):
                posts.append(post)
            break
        except ConnectionError:
            continue

    # analyze posts
    for i, post in enumerate(posts):

        # ad must be available
        if not post['available']:
            continue

        if (
            not "listing_location" in post.keys()
        ):  # if not a listing, continue to next post
            continue

        # get post_text, remove uppercase and punctuation. One version with ., and one without
        (text, text_with_dot) = cleanup(
            post
        )

        onlygirls = False
        if only_girls(text):
            onlygirls = True

        tijdelijk = check_tijdelijk(text)

        size = extract_size(
            text, text_with_dot
        )  # TODO: sometimes, size is with dot. ex, 11.5m2. Should take care of that.

        (postcode, streets, buurts_en_wijken) = extract_location(post, text)

        price = post["listing_price"][1:]

        print(
            f"""post {i}: size:{size}, only_girls:{onlygirls}, price:{price}, tijdelijk: {tijdelijk}
            location:{postcode, streets, buurts_en_wijken} \n"""
        )

        # analyze location
        success = location_evaluator(postcodes_of_interest, postcode, streets, buurts_en_wijken)

        if (
            (size == None or size > min_size) #for now, give benefit of the doubt
            and price != None
            and float(price.replace(",", "")) <= max_price
            and success != None
            and success
        ):
            print("hurray! found a match")
            matches.append(i)

    with open("matches.pickle", "wb") as f:
        pickle.dump(matches, f)
        
    return posts, matches


    #TODO: send_post_to_email(post)
if __name__ == '__main__':

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
    posts, matches = run(max_price=700, min_size=20, postcodes_of_interest=postcodes_of_interest)
