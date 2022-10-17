# Flask app

# Dependencies 

from flask import Flask, render_template, redirect

# Instantiate flask app

app = Flask(__name__)


# Flask routes

@app.route("/")
def index():    

    

    return render_template("index.html")

@app.route("/search")
def search():



    return redirect("/", code=302)

@app.route("/results")
def results():



    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)