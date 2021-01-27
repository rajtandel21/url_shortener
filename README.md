# URL Shortener

This app was created using Python and Flask

## Note

- If the database is not found follow these steps
- In `pipenv shell` enter `python`
- This will enter you into the python shell
- `import server imporot init_db`
- `init_db`
- This will initialize the database for use.

## How to Run:

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
