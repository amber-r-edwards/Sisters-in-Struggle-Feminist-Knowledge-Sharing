from flask import Flask, render_template
import sqlite3
import os

# Initialize the Flask application
app = Flask(__name__)

# Path to the SQLite database file
DB_PATH = '../zines.db'  # Back one folder and just the name

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
    """
    Home page route - displays a list of events
    
    This is the main page of our web application. When someone visits
    the root URL (http://localhost:5000/), this function runs.
    
    What this function does:
    1. Connects to the database
    2. Runs a SQL query to get event information
    3. Closes the database connection
    4. Renders an HTML template with the data
    
    Returns:
        HTML page: The rendered index.html template with event data
    """
    # Get a connection to our database
    conn = get_db_connection()
    
    # Execute a SQL query to get event data
    # This query:
    # - SELECTs all columns from events (e) and publication details from publications (p)
    # - JOINs the events and publications tables on publication_id
    # - FILTERs out events with empty or null titles
    # - LIMITs results to 10 events
    events = conn.execute('''
        SELECT e.event_title, e.event_date, e.city, e.state, e.country,
               p.pub_title AS publication_title, p.volume AS volume_number, 
               p.issue_number AS issue_number
        FROM events e
        LEFT JOIN publications p ON e.publication_id = p.pub_id
        WHERE e.event_title IS NOT NULL AND e.event_title != ''
    ''').fetchall()  # fetchall() gets all the results as a list of Row objects
    
    # Always close database connections when done
    conn.close()
    
    # Render the HTML template and pass the events data to it
    # The template can access the 'events' variable
    return render_template('index.html', events=events)

if __name__ == '__main__':
    # Start the Flask development server
    # Parameters explained:
    # - debug=True: Enables debug mode (auto-reloads on changes, shows detailed errors)
    # - host='0.0.0.0': Makes the server accessible from any IP address
    # - port=5000: Runs on port 5000
    app.run(debug=True, host='0.0.0.0', port=5001)