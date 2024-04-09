# Spendendings

A very creative tool with a very uncreative name.

## Description

## Setup

``` bash
git clone https://github.com/Fabs37/spendendings.git
cd spendendings
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
flask -A spendendings init-db
```

## Deploying

### [Development server](https://flask.palletsprojects.com/en/3.0.x/server/)

By default, it is listening on [127.0.0.1:5000](127.0.0.1:5000).

``` bash
flask -A spendendings run
```

### Quick and (kinda) dirty
This approach uses [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/index.html) as server. See also [the Flask documentation](https://flask.palletsprojects.com/en/3.0.x/deploying/waitress/).

``` bash
python3 serve.py 8080
```

### How you *should* do it

See the [Flask doc](https://flask.palletsprojects.com/en/3.0.x/deploying/).

## Command Line

The following command line scripts are available (the server isn't required to be running while executing them):

- `flask -A spendendings add-project NAME GOAL ESTIMATEDCONTRIBUTORS`
- `flask -A spendendings delete-project UUID`
- `flask -A spendendings update-project UUID NAME GOAL ESTIMATEDCONTRIBUTORS`
- `flask -A spendendings list-projects`
- `flask -A spendendings init-db`

    Initializes the database (should be at `instance/spendendings.sqlite`, `.venv/var/spendendings-instance/spendendings.sqlite` or somewhere else). Modifying this database directly makes the other commands quite obsolete. **Warning**: Running this command (more precisely, [/spendendings/schema.sql](/spendendings/schema.sql)) again later will reset the database, deleting all existing data.

- `flask -A spendendings inject-sql FILENAME`

    Executes the given SQL file on the database mentioned above. Use with caution.

