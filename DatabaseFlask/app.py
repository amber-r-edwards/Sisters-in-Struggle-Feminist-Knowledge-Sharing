from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = '../zines.db' #back one folder and just the name

def get_db_connection():
    """
    Create a connection to the SQLite database
    
    This function:
    1. Opens a connection to the database file
    2. Sets row_factory to sqlite3.Row so we can access columns by name
       (instead of just by index number)
    3. Returns the connection object
    
    Returns:
        sqlite3.Connection: A database connection object
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name like row['title']
    return conn

@app.route('/')
def index():
    conn = get_db_connection #get connection to database
    events = conn.execute('''
         SELECT e.*,  
            p.pub_title AS publication_title,
            p.volume AS volume_number,
            p.issue_number AS issue_number
         FROM 
            events e
         LEFT JOIN 
            publications p
         ON 
            e.publication_id = p.pub_id;
    ''').fetchall()
    conn.close()
    return render_template('index.html', events=events)