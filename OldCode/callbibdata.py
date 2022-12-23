import isbnlib as il
import requests
from bs4 import BeautifulSoup

def get_oclc_code(a_dict):
    """
        Performs first requests call to OCLC Classify and gets response code and soup.

        RESPONSE CODES:
        2 = single-work
        4 = multi-work
        102 = no record in oclc

        Returns response_code, soup, isbn13.

    """
    an_isbn = a_dict.get("ISBN-13")
    firstscrape_url = "http://classify.oclc.org/classify2/Classify"
    firstscrape_params = {"isbn": an_isbn, "summary": "false", "maxrecs": 1}

    try:
        first_rec = requests.get(firstscrape_url, params=firstscrape_params)
        first_soup = BeautifulSoup(first_rec.text, "lxml")

    except:
        return 0, None, an_isbn

    try:
        if response_code := first_soup.select("response")[0].get("code"):
            return response_code, first_soup, an_isbn

        else:
            return 0, first_soup, an_isbn

    except:
        return 0, first_soup, an_isbn

def get_isbn(user_input):
    """
        Calls isbnlib to get working isbn13 from user_input (isbn or title words).
        Returns a working isbn13.

    """

    if il.is_isbn13(user_input):
        return user_input

    elif il.is_isbn10(user_input):
        return il.to_isbn13(user_input)

    elif il.notisbn(user_input):
        try:
            working_isbn = il.isbn_from_words(user_input)
            return working_isbn

        except:
            return "9781886101111"

def get_api_data(an_isbn):
    """
            Calls Google Books api and OCLC Classify api and fills in missing values in master_dict.
            Returns master_dict.

    """
    user_isbn = an_isbn

    desired_dict = {
        "ISBN-13": an_isbn, 
        "Title": "", 
        "Authors": [],
        "owi": "", 
        "lcc": "", 
        "fast": {}, 
        "bookcover_url": ""
                   }

    if gbooks_dict := il.meta(user_isbn, service="goob"):        
        for k,v in gbooks_dict.items():
            if k in desired_dict:
                desired_dict[k] = v
    
    if classify_dict := il.classify(user_isbn):
        for k, v in classify_dict.items():
            if k in desired_dict:
                desired_dict[k] = v    

    return desired_dict