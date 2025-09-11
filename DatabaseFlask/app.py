from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
import secrets 

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generates a 32-character random key

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
    Home page route - displays a paginated list of events in a table format.
    
    This is the main page of our web application. When someone visits
    the root URL (http://localhost:5001/), this function runs.
    
    What this function does:
    1. Connects to the database
    2. Runs a SQL query to get event information, including pagination
    3. Closes the database connection
    4. Renders an HTML template with the data
    
    Returns:
        HTML page: The rendered index.html template with event data
    """
    # Get the current page number from the query parameters (default to 1)
    page = int(request.args.get('page', 1))
    per_page = 10  # Number of events per page
    offset = (page - 1) * per_page  # Calculate the offset for the SQL query

    # Get a connection to our database
    conn = get_db_connection()
    
    # Execute a SQL query to get event data with pagination
    events = conn.execute('''
        SELECT e.event_title, e.event_date, e.city, e.state, e.country, e.event_type,
               e.description, e.location, e.address, e.source_publication,
               p.pub_title AS publication_title, p.volume AS volume_number, 
               p.issue_number AS issue_number
        FROM events e
        LEFT JOIN publications p ON e.publication_id = p.pub_id
        WHERE e.event_title IS NOT NULL AND e.event_title != ''
        LIMIT ? OFFSET ?
    ''', (per_page, offset)).fetchall()  # fetchall() gets all the results as a list of Row objects

    # Get the total number of events for pagination
    total_events = conn.execute('SELECT COUNT(*) FROM events').fetchone()[0]
    conn.close()

    # Calculate the total number of pages
    total_pages = (total_events + per_page - 1) // per_page  # Round up division

    # Render the HTML template and pass the events data and pagination info to it
    return render_template('index.html', events=events, page=page, total_pages=total_pages)

@app.route('/add_publication', methods=['GET', 'POST'])
def add_publication():
    """
    Add new publication route - handles both displaying form and processing submission
    
    GET: Shows the form to add a new publication
    POST: Processes the form data and adds publication to the database
    
    Returns:
        HTML page: Either the form (GET) or redirect to home page (POST)
    """
    if request.method == 'POST':
        # Handle form submission
        return handle_publication_submission()
    else:
        # Display the form
        return show_publication_form()

def show_publication_form():
    """
    Display the form for adding a new publication
    
    Returns:
        HTML page: The publication form
    """
    return render_template('add_publication.html')

def handle_publication_submission():
    """
    Process the form data and add new publication to the database
    
    Returns:
        Redirect: To home page with success/error message
    """
    # Get form data
    pub_title = request.form.get('pub_title', '').strip()
    volume = request.form.get('volume', '').strip()
    issue_number = request.form.get('issue_number', '').strip()
    
    # Basic validation
    if not pub_title:
        flash('Publication title is required!', 'error')
        return redirect(url_for('add_publication'))
    
    try:
        conn = get_db_connection()
        
        # Insert the new publication
        conn.execute('''
            INSERT INTO publications (pub_title, volume, issue_number)
            VALUES (?, ?, ?)
        ''', (pub_title, volume, issue_number))
        
        # Commit the changes
        conn.commit()
        conn.close()
        
        # Success message
        flash(f'Successfully added publication: {pub_title}', 'success')
        
    except Exception as e:
        flash(f'Error adding publication: {str(e)}', 'error')
    
    # Redirect back to home page
    return redirect(url_for('index'))

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    """
    Add new event route - handles both displaying form and processing submission
    
    GET: Shows the form to add a new event
    POST: Processes the form data and adds event to the database
    
    Returns:
        HTML page: Either the form (GET) or redirect to home page (POST)
    """
    if request.method == 'POST':
        # Handle form submission
        return handle_event_submission()
    else:
        # Display the form
        return show_event_form()

def show_event_form():
    """
    Display the form for adding a new event
    
    Returns:
        HTML page: The event form
    """
    return render_template('add_event.html')

def handle_event_submission():
    """
    Process the form data and add new event to the database
    
    Returns:
        Redirect: To home page with success/error message
    """
    # Get form data
    event_title = request.form.get('event_title', '').strip()
    event_date = request.form.get('event_date', '').strip()
    city = request.form.get('city', '').strip()
    state = request.form.get('state', '').strip()
    country = request.form.get('country', '').strip()
    publication_id = request.form.get('publication_id', '').strip()
    
    # Basic validation
    if not event_title:
        flash('Event title is required!', 'error')
        return redirect(url_for('add_event'))
    
    try:
        conn = get_db_connection()
        
        # Insert the new event
        conn.execute('''
            INSERT INTO events (event_title, event_date, city, state, country, publication_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (event_title, event_date, city, state, country, publication_id))
        
        # Commit the changes
        conn.commit()
        conn.close()
        
        # Success message
        flash(f'Successfully added event: {event_title}', 'success')
        
    except Exception as e:
        flash(f'Error adding event: {str(e)}', 'error')
    
    # Redirect back to home page
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Start the Flask development server
    # Parameters explained:
    # - debug=True: Enables debug mode (auto-reloads on changes, shows detailed errors)
    # - host='0.0.0.0': Makes the server accessible from any IP address
    # - port=5000: Runs on port 5000
    app.run(debug=True, host='0.0.0.0', port=5001)

