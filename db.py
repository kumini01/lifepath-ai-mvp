import sqlite3
from pathlib import Path

DB_PATH = Path('data/lifepath.db')
DB_PATH.parent.mkdir(exist_ok=True)

def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with conn() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS profile(id INTEGER PRIMARY KEY CHECK(id=1), name TEXT, birth_year INTEGER, job_status TEXT, interests TEXT);
        CREATE TABLE IF NOT EXISTS life_events(id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL, title TEXT NOT NULL, event_date TEXT, memo TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS todos(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, due_date TEXT, done INTEGER DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
        CREATE TABLE IF NOT EXISTS family_members(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, relation TEXT, birth_year INTEGER);
        ''')

def save_profile(name, birth_year, job_status, interests):
    with conn() as c:
        c.execute('INSERT INTO profile(id,name,birth_year,job_status,interests) VALUES(1,?,?,?,?) ON CONFLICT(id) DO UPDATE SET name=excluded.name,birth_year=excluded.birth_year,job_status=excluded.job_status,interests=excluded.interests', (name,birth_year,job_status,interests))

def get_profile():
    with conn() as c: return c.execute('SELECT * FROM profile WHERE id=1').fetchone()

def add_event(category,title,event_date,memo):
    with conn() as c: c.execute('INSERT INTO life_events(category,title,event_date,memo) VALUES(?,?,?,?)',(category,title,event_date,memo))

def get_events():
    with conn() as c: return c.execute('SELECT * FROM life_events ORDER BY event_date DESC, id DESC').fetchall()

def delete_event(i):
    with conn() as c: c.execute('DELETE FROM life_events WHERE id=?',(i,))

def add_todo(title,due_date):
    with conn() as c: c.execute('INSERT INTO todos(title,due_date) VALUES(?,?)',(title,due_date))

def get_todos():
    with conn() as c: return c.execute('SELECT * FROM todos ORDER BY done, due_date, id DESC').fetchall()

def set_todo(i,done):
    with conn() as c: c.execute('UPDATE todos SET done=? WHERE id=?',(int(done),i))

def add_family(name,relation,birth_year):
    with conn() as c: c.execute('INSERT INTO family_members(name,relation,birth_year) VALUES(?,?,?)',(name,relation,birth_year))

def get_family():
    with conn() as c: return c.execute('SELECT * FROM family_members ORDER BY id DESC').fetchall()
