DROP TABLE IF EXISTS donation;
DROP TABLE IF EXISTS project;

CREATE TABLE donation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT NOT NULL,
    alias TEXT NOT NULL,
    lower INTEGER NOT NULL,
    upper INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES project (uuid)
);

CREATE TABLE project (
    uuid TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    goal INTEGER NOT NULL,
    estimated_contributors INTEGER NOT NULL,
    min_donation INTEGER,
    max_donation INTEGER,
    pw_hash TEXT
);
