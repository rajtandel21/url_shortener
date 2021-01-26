# URL Shortener

This app was created using Python and Flask

# How to Run:

- fork and git clone this repo.
- cd into the folder
- pipenv install -r requirements.txt
- pipenv shell
- Tell terminal which application to work with:
  - export FLASK_APP=server.py (Linux/MacOS/GitBash)
  - set FLASK_APP=server.py (Windows Command Prompt)
  - $env:FLASK_APP = "server.py" (PowerShell)
- Tell terminal which environment to work in:
  - export FLASK_ENV=development (Linux/MacOS/GitBash)
  - set FLASK_ENV=development (Windows Command Prompt)
  - $env:FLASK_ENV="development" (PowerShell)
- flask run
