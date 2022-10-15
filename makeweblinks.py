import urllib.parse

def make_links(a_dict):
    primosearch_base_url = "mnpals-mct.primo.exlibrisgroup.com/discovery/search"
    primosearch_params = "&tab=Everything&search_scope=MyInst_and_CI&sortby=rank&vid=01MNPALS_MCT:MCT&mode=advanced"

    primobrowse_base_url = "mnpals-mct.primo.exlibrisgroup.com/discovery/browse"
    primobrowse_params = "?vid=01MNPALS_MCT:MCT&browseScope=callnumber.0&innerPnxIndex=-1&numOfUsedTerms=-1&fn=BrowseSearch&browseQuery="

    fod_base_url = "mctproxy.mnpals.net/login?url=https://fod.infobase.com/PortalPlaylists.aspx"
    fod_params = "?bc=0&rd=a&wID=103688&q="

    gbooks_base_url = "www.google.com/search?tbo=p&tbm=bks&q=isbn:"
    worldcat_base_url = "www.worldcat.org/search?q=bn:"

    library_links = {}

    if the_isbn := a_dict.get("ISBN-13"):
        library_links["Primo_ISBN = " + the_isbn] = "https://" + primosearch_base_url + "?query=isbn,exact," \
                                                    + the_isbn + primosearch_params
        library_links["GoogleBooks_ISBN = " + the_isbn] = "https://" + gbooks_base_url + the_isbn
        library_links["WorldCat_ISBN = " + the_isbn] = "https://" + worldcat_base_url + the_isbn

    if the_title := a_dict.get("Title"):
        library_links["Primo_Title = " + the_title] = "https://" + primosearch_base_url + "?query=title,exact,"\
                                                      + urllib.parse.quote(the_title) + primosearch_params

    if the_lcc := a_dict.get("lcc"):
        library_links["Primo_LCC = " + the_lcc] = "https://" + primobrowse_base_url + primobrowse_params \
                                                  + urllib.parse.quote(the_lcc)

    if the_authors := a_dict.get("Authors"):
        for author in the_authors:
            library_links["Primo_Author = " + author] = "https://" + primosearch_base_url + "?query=any,exact," \
                                                        + urllib.parse.quote(author) + primosearch_params
            library_links["FilmsOnDemand_Author = " + author] = "https://" + fod_base_url + fod_params \
                                                                + urllib.parse.quote(author)

    if the_subjects := a_dict.get("fast"):
        for fastnum, subject in the_subjects.items():
            library_links["Primo_Subject = " + subject] = "https://" + primosearch_base_url + "?query=sub,exact," \
                                                          + urllib.parse.quote(subject) + primosearch_params
            library_links["FilmsOnDemand_Subject = " + subject] = "https://" + fod_base_url + fod_params \
                                                                  + urllib.parse.quote(subject)

    print_links = {tag:library_links[tag] for tag in sorted(library_links.keys(), key=str.lower, reverse=True)}

    return print_links