from flask import Flask

server = Flask(__name__)


@server.route('/')
def home():
    return 'welcome to url shortener website'

server.run(debug=True)
