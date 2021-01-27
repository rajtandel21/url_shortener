from flask import Flask, render_template, request, g, redirect
from db import get_db
import string
import random

server = Flask(__name__)


@server.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#app is the flask app we defined
def init_db():
    with server.app_context():
        db = get_db()
        with server.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


#@server.route('/table')
#def stuff():
#    db = get_db()
#    cursor = db.cursor()
#    cursor.execute("SELECT * from urls")
#   trees = cursor.fetchall()
#
#    return "new.html"

def random_short():
    letters = string.ascii_lowercase + string.ascii_uppercase
    rand_letter = random.choices(letters, k=5)
    rand_letter = "".join(rand_letter)
    #check db for if this rand letters already exist
    return rand_letter

@server.route('/', methods=['GET', 'POST'])
def home():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        longurl = request.form["nm"]
        print(longurl)
        cursor.execute("SELECT COUNT(*) FROM urls WHERE longurl=(?);", (longurl,))
        url_exists = cursor.fetchone()[0]
        print(url_exists)
        if url_exists > 0:
            message = "This url already exists"
            return render_template("input.html", title="Home", message=message)
        
        shorturl = random_short()
        #print(shorturl)
        cursor.execute("INSERT INTO urls (longurl, shorturl) VALUES (?, ?);", (longurl, shorturl))
        db.commit()

        #message = f"short url {shorturl} was created for {longurl}!"
        #return render_template('input.html', title="Home", message=message)

    cursor.execute('SELECT * FROM urls')
    all_urls = cursor.fetchall()
    #print(all_urls)
    message= "create a url"
    return render_template("input.html", title="Home", message=message, all_urls=all_urls)


@server.route('/all')
def allurls():
    return "all urls will be here"

#localshost:5000/askdh
#google.co.uk

@server.route('/<string:url>', methods=['GET'])
def reroute(url):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM urls WHERE shorturl=(?);", (url,))
    og_url = cursor.fetchall()[0]
    if og_url == 0:
        return "This short url does not exist"
    print(og_url[1])
    return redirect(og_url[1], code=302)

@server.errorhandler(404)
def handle_404(err):
        return render_template("404.html", title="Oops"), 404


if __name__ == "__main__":
    server.run(port=5000, debug=True)
