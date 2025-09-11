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
    Home page route - displays a searchable, sortable, and filterable list of events in a table format.
    """
    # Get query parameters for search, sorting, and filtering
    search = request.args.get('search', '').strip()
    sort = request.args.get('sort', 'event_title')  # Default sort by event_title
    order = request.args.get('order', 'asc')  # Default order is ascending
    city_filter = request.args.get('city', '').strip()
    state_filter = request.args.get('state', '').strip()
    event_type_filter = request.args.get('event_type', '').strip()

    # Get the current page number from the query parameters (default to 1)
    page = int(request.args.get('page', 1))
    per_page = 10  # Number of events per page
    offset = (page - 1) * per_page  # Calculate the offset for the SQL query

    # Build the SQL query dynamically
    query = '''
        SELECT e.event_id, e.event_title, e.event_date, e.city, e.state, e.country, e.event_type,
               e.description, e.location, e.address, e.source_publication,
               p.pub_title AS publication_title, p.volume AS volume_number, 
               p.issue_number AS issue_number
        FROM events e
        LEFT JOIN publications p ON e.publication_id = p.pub_id
        WHERE 1=1
    '''
    params = []

    # Add search functionality
    if search:
        query += " AND (e.event_title LIKE ? OR e.description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    # Add filtering functionality for city and state as search fields
    if city_filter:
        query += " AND e.city LIKE ?"
        params.append(f"%{city_filter}%")
    if state_filter:
        query += " AND e.state LIKE ?"
        params.append(f"%{state_filter}%")
    if event_type_filter:
        query += " AND e.event_type = ?"
        params.append(event_type_filter)
    if request.args.get('country', '').strip():
        country_filter = request.args.get('country', '').strip()
        query += " AND e.country LIKE ?"
        params.append(f"%{country_filter}%")

    # Add sorting functionality
    if sort in ['event_title', 'event_date', 'city', 'state', 'event_type']:
        query += f" ORDER BY {sort} {order.upper()}"

    # Add pagination
    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, offset])

    # Get a connection to our database
    conn = get_db_connection()
    events = conn.execute(query, params).fetchall()

    # Get the total number of events for pagination
    total_query = "SELECT COUNT(*) FROM events e WHERE 1=1"
    if search:
        total_query += " AND (e.event_title LIKE ? OR e.description LIKE ?)"
    if city_filter:
        total_query += " AND e.city LIKE ?"
    if state_filter:
        total_query += " AND e.state LIKE ?"
    if event_type_filter:
        total_query += " AND e.event_type = ?"
    total_events = conn.execute(total_query, params[:-2]).fetchone()[0]  # Exclude LIMIT and OFFSET params
    conn.close()

    # Calculate the total number of pages
    total_pages = (total_events + per_page - 1) // per_page  # Round up division

    # Render the HTML template and pass the events data and pagination info to it
    return render_template(
        'index.html',
        events=events,
        page=page,
        total_pages=total_pages,
        search=search,
        sort=sort,
        order=order,
        city_filter=city_filter,
        state_filter=state_filter,
        event_type_filter=event_type_filter
    )

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

@app.route('/edit/<string:record_type>/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_type, record_id):
    """
    Edit page for either events or publications.

    Args:
        record_type (str): The type of record to edit ('event' or 'publication').
        record_id (int): The ID of the record to edit.

    Returns:
        HTML page: The edit form (GET) or redirects back to the index page after saving changes (POST).
    """
    conn = get_db_connection()

    # Check if the record type is valid
    if record_type not in ['event', 'publication']:
        flash('Invalid record type!', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Handle form submission to update the record
        if record_type == 'event':
            event_title = request.form.get('event_title', '').strip() or 'NA'
            event_date = request.form.get('event_date', '').strip() or 'NA-NA-NA'
            city = request.form.get('city', '').strip() or 'NA'
            state = request.form.get('state', '').strip() or 'NA'
            country = request.form.get('country', '').strip() or 'NA'
            event_type = request.form.get('event_type', '').strip() or 'NA'
            description = request.form.get('description', '').strip() or 'NA'

            # Update the event in the database
            conn.execute('''
                UPDATE events
                SET event_title = ?, event_date = ?, city = ?, state = ?, country = ?, event_type = ?, description = ?
                WHERE event_id = ?
            ''', (event_title, event_date, city, state, country, event_type, description, record_id))
            conn.commit()
            flash('Event updated successfully!', 'success')

        elif record_type == 'publication':
            pub_title = request.form.get('pub_title', '').strip() or 'NA'
            volume = request.form.get('volume', '').strip() or 'NA'
            issue_number = request.form.get('issue_number', '').strip() or 'NA'
            issue_date = request.form.get('issue_date', '').strip() or 'NA'
            author_org = request.form.get('author_org', '').strip() or 'NA'
            location = request.form.get('location', '').strip() or 'NA'

            # Update the publication in the database
            conn.execute('''
                UPDATE publications
                SET pub_title = ?, volume = ?, issue_number = ?, issue_date = ?, author_org = ?, location = ?
                WHERE pub_id = ?
            ''', (pub_title, volume, issue_number, issue_date, author_org, location, record_id))
            conn.commit()
            flash('Publication updated successfully!', 'success')

        conn.close()

        # Redirect back to the index page
        return redirect(url_for('index'))

    else:
        # Handle GET request to display the edit form
        if record_type == 'event':
            record = conn.execute('SELECT * FROM events WHERE event_id = ?', (record_id,)).fetchone()
        elif record_type == 'publication':
            record = conn.execute('SELECT * FROM publications WHERE pub_id = ?', (record_id,)).fetchone()

        conn.close()

        if not record:
            flash('Record not found!', 'error')
            return redirect(url_for('index'))

        return render_template('edit.html', record=record, record_type=record_type)

if __name__ == '__main__':
    # Start the Flask development server
    # Parameters explained:
    # - debug=True: Enables debug mode (auto-reloads on changes, shows detailed errors)
    # - host='0.0.0.0': Makes the server accessible from any IP address
    # - port=5000: Runs on port 5000
    app.run(debug=True, host='0.0.0.0', port=5001)

