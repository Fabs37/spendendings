import sqlite3

import click, uuid
from flask import current_app, g, Flask
from tabulate import tabulate


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()
        
def init_db():
    db = get_db()
    
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')
    
@click.command('inject-sql')
@click.argument('filename', type=str)
def inject_sql_command(filename: str):
    db = get_db()
    with current_app.open_resource(filename) as f:
        db.executescript(f.read().decode('utf8'))
        
@click.command("add-project")
@click.argument('name', type=str)
@click.argument('goal', type=int)
@click.argument('estimatedcontributors', type=int)
def add_project_cmd(name, goal, estimatedcontributors):
    newUuid = str(uuid.uuid4())
    get_db().execute("INSERT INTO project (uuid, title, goal, estimated_contributors) VALUES (?, ?, ?, ?)", (
        newUuid,
        name,
        goal,
        estimatedcontributors,
    ))
    get_db().commit()
    click.echo(f"Created project '{name}' with UUID '{newUuid}', accessible via /project/{newUuid}.")
    
@click.command("update-project")
@click.argument('projectuuid', type=click.UUID)
@click.argument('name', type=str)
@click.argument('goal', type=int)
@click.argument('estimatedcontributors', type=int)
def update_project_cmd(projectuuid, name, goal, estimatedcontributors):
    get_db().execute("UPDATE project SET title = ?, goal = ?, estimated_contributors = ? WHERE uuid = ?", (
        name,
        goal,
        estimatedcontributors,
        str(projectuuid),
    ))
    get_db().commit()
    click.echo("Update successful.")
    
@click.command("delete-project")
@click.argument('projectuuid', type=click.UUID)
def delete_project_cmd(projectuuid):
    get_db().execute("DELETE FROM donation WHERE project_id = ?", (str(projectuuid),))
    get_db().commit()
    get_db().execute("DELETE FROM project WHERE uuid = ?", (
        str(projectuuid),
    ))
    get_db().commit()
    click.echo("Deleted the project and all linked donations.")
    
@click.command("list-projects")
def list_projects_cmd():
    click.echo(tabulate(
        get_db().execute("SELECT uuid, title, goal, estimated_contributors FROM project"),
        ["UUID", "Title", "Goal", "Estimated contributors"],
        tablefmt="pretty"
    ))

def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(inject_sql_command)
    app.cli.add_command(add_project_cmd)
    app.cli.add_command(update_project_cmd)
    app.cli.add_command(delete_project_cmd)
    app.cli.add_command(list_projects_cmd)