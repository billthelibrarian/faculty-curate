import re
import requests
from bs4 import BeautifulSoup
from html import unescape
from callbibdata import get_oclc_code

def make_title(work_tag):
    try:
        title = unescape(work_tag.get("title"))

    except:
        title = ""

    return title

def make_authors(work_tag):
    try:
        author = work_tag.get("author")

    except:
        return []

    bracket_regx = re.compile(r"\[(.*?)\]")

    try:
        dedupe_list = list(set(author.split(" | ")))      # dedupe
        author_list = list(set([re.sub(bracket_regx, "", author).strip() for author in dedupe_list]))
        # to deal with isbn 9781584806844 issue

    except:
        author_list = []

    return author_list

def make_oclcnums(work_tag):
    try:
        owi = work_tag.get("owi")
        wi = work_tag.get("wi")

    except:
        owi = ""
        wi = ""

    return owi, wi

def scrape_singlework(a_soup, an_isbn):
    """
        Performs scrape when response code = 2 (single-work), returns singlework_dict.

    """
    isbn13 = an_isbn

    try:
        first_worktag = a_soup.work

    except:
        first_worktag = ""

    title = make_title(first_worktag)
    owi, wi = make_oclcnums(first_worktag)
    author_list = make_authors(first_worktag)

    ############################
    def make_lcc():
        try:
            lcc = a_soup.lcc.mostpopular.get("sfa", a_soup.lcc.mostrecent.get("sfa"))
            if lcc is None:
                lcc = a_soup.lcc.mostpopular.get("nsfa", a_soup.lcc.mostrecent.get("nsfa"))

        except AttributeError as e:
            lcc = ""

        return lcc
    ############################

    lcc = make_lcc()

    ############################
    def make_subjects():
        fast = {}
        subj_list = []
        fastnum_list = []

        try:
            subj_tags = a_soup.find_all("heading")
            if subj_tags:
                for tag in subj_tags:
                    fast[tag.get("ident")] = tag.string

            else:
                sh_table = a_soup.find("table", id="subheadtbl")
                sh_links = sh_table.find_all("a")
                for link in sh_links:
                    if link.string.isnumeric():
                        fastnum_list.append(link.string)

                    else:
                        subj_list.append(link.string)

                fast = dict(zip(fastnum_list, subj_list))

        except AttributeError as e:
            return {}

        return fast
    ############################

    fast = make_subjects()

    singlework_dict = {
        "ISBN-13": an_isbn, 
        "Title": title, 
        "Authors": author_list,
        "owi": owi, 
        "wi": wi, 
        "lcc": lcc, 
        "fast": fast
                      }

    return singlework_dict



def scrape_multiwork(a_soup, an_isbn):
    """
        Performs scrape when response code = 4 (multi-work), returns multiwork_dict.

    """

    try:
        first_worktag = a_soup.work

    except:
        first_worktag = ""

    title = make_title(first_worktag)
    owi, wi = make_oclcnums(first_worktag)
    author_list = make_authors(first_worktag)

    multiwork_dict = {
        "ISBN-13": an_isbn, 
        "Title": title, 
        "Authors": author_list,
        "owi": owi, 
        "wi": wi, 
        "lcc": "", 
        "fast": {}
                     }

    secondscrape_url = "http://classify.oclc.org/classify2/ClassifyDemo"
    secondscrape_params = {"owi": owi, "wi": wi}

    try:
        second_rec = requests.get(secondscrape_url, params=secondscrape_params)
        second_soup = BeautifulSoup(second_rec.text, "lxml")

    except:
        return multiwork_dict

    ############################
    def make_lcc():
        try:
            lcc = (second_soup.find("td", {"class":"tag"}, text="050")).next_sibling.get_text()

        except AttributeError as e:

            try:
                lcc_str = (second_soup.find("a", text="ClassWeb")).attrs["href"]
                start_pos = lcc_str.find("iterm=")
                end_pos = lcc_str.find("&", start_pos)
                lcc = lcc_str[start_pos+6:end_pos]

            except AttributeError as e:
                lcc = ""

        return lcc
    ############################


    ############################
    def make_subjects():

        subj_list = []
        fastnum_list = []
        fast = {}

        try:
            sh_table = second_soup.find("table", id="subheadtbl")
            sh_links = sh_table.find_all("a")
            for link in sh_links:
                if link.string.isnumeric():
                    fastnum_list.append(link.string)

                else:
                    subj_list.append(link.string)

            fast = dict(zip(fastnum_list, subj_list))

        except:
            return {}

        return fast
    ############################

    multiwork_dict["fast"] = make_subjects()
    multiwork_dict["lcc"] = make_lcc()

    return multiwork_dict


def code_dispatch(a_dict):

    resp_code, f_soup, the_isbn = get_oclc_code(a_dict)

    if resp_code == "102":
        return a_dict

    elif resp_code == "2":
        return scrape_singlework(f_soup, the_isbn)

    elif resp_code == "4":
        return scrape_multiwork(f_soup, the_isbn)