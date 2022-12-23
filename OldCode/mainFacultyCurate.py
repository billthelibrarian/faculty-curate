from callbibdata import get_isbn, get_api_data
from makeweblinks import make_links
from flask import Flask, render_template, request, redirect
import isbnlib as il

app = Flask(__name__)

##########################################################

@app.route("/")
@app.route("/entry_page")
def entry_page():

    the_title = "Welcome to Faculty Curate!"
    return render_template("entry.html", the_title=the_title)

##########################################################

##########################################################
@app.route("/bad_results")
def bad_results():

    the_title = "DRATS!"
    return render_template("badresults.html", the_title=the_title)

##########################################################

##########################################################
@app.route("/do_search", methods=["POST"])
def do_search():

    if request.method != "POST":
        return redirect("/")

    else:
        isbn_input = request.form["isbn_input"]

        if isbn_input:
            isbn13 = get_isbn(isbn_input.strip())
            img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/480px-No_image_available.svg.png"
            try:
                bookcover_url = il.cover(isbn13).get("thumbnail", img_url)
            except:
                bookcover_url = img_url

            api_dict = get_api_data(isbn13)
            
            print_links = make_links(api_dict)
            return render_template(

                    "results.html",
                    the_title="Here are your results:",
                    isbn13=isbn13,
                    the_results_links=print_links,
                    bookcover_url=bookcover_url

                                 )            
            
        else:
            return redirect("/")

#########################################################

if __name__ == "__main__":
    app.run()

