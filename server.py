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



def random_short():
    db = get_db()
    cursor = db.cursor()
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letter = random.choices(letters, k=5)
        rand_letter = "".join(rand_letter)
        cursor.execute("SELECT COUNT(*) FROM urls WHERE shorturl=(?);", (rand_letter,))
        url_exists = cursor.fetchone()[0]
        if not url_exists > 0:
            return rand_letter
    #check db for if this rand letters already exist

@server.route('/', methods=['GET', 'POST'])
def home():
    db = get_db()
    cursor = db.cursor()
    if request.method == 'POST':
        longurl = request.form["nm"]
        test_list = ['.com', '.co.uk', '.io']
        print(longurl)
        #res = [ele for ele in test_list if(ele in longurl)]
        #print(res)
        if not any(word in longurl for word in test_list):
            return render_template("input.html", title="Home", message="url end is not valid")
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
