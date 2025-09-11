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
    Home page route - displays paginated lists of events and publications in separate tables.
    """
    # Get query parameters for events
    search = request.args.get('search', '').strip()
    sort_events = request.args.get('sort_events', 'event_title')  # Default sort for events
    order_events = request.args.get('order_events', 'asc')  # Default order for events
    page_events = int(request.args.get('page_events', 1))  # Current page for events
    per_page = 10  # Number of rows per page
    offset_events = (page_events - 1) * per_page

    # Get query parameters for publications
    sort_publications = request.args.get('sort_publications', 'pub_title')  # Default sort for publications
    order_publications = request.args.get('order_publications', 'asc')  # Default order for publications
    page_publications = int(request.args.get('page_publications', 1))  # Current page for publications
    offset_publications = (page_publications - 1) * per_page

    # Get a connection to the database
    conn = get_db_connection()

    # Query for events with pagination
    events_query = f'''
        SELECT e.event_id, e.event_title, e.event_date, e.city, e.state, e.country, e.event_type,
               e.description, e.location, e.address, e.source_publication,
               p.pub_title AS publication_title
        FROM events e
        LEFT JOIN publications p ON e.publication_id = p.pub_id
        WHERE e.event_title LIKE ?
        ORDER BY {sort_events} {order_events.upper()}
        LIMIT ? OFFSET ?
    '''
    events = conn.execute(events_query, (f"%{search}%", per_page, offset_events)).fetchall()

    # Total number of events for pagination
    total_events_query = '''
        SELECT COUNT(*) FROM events WHERE event_title LIKE ?
    '''
    total_events = conn.execute(total_events_query, (f"%{search}%",)).fetchone()[0]

    # Query for publications with pagination
    publications_query = f'''
        SELECT pub_id, pub_title, volume, issue_number, issue_date, author_org, location
        FROM publications
        ORDER BY {sort_publications} {order_publications.upper()}
        LIMIT ? OFFSET ?
    '''
    publications = conn.execute(publications_query, (per_page, offset_publications)).fetchall()

    # Total number of publications for pagination
    total_publications_query = '''
        SELECT COUNT(*) FROM publications
    '''
    total_publications = conn.execute(total_publications_query).fetchone()[0]

    conn.close()

    # Calculate total pages for events and publications
    total_pages_events = (total_events + per_page - 1) // per_page  # Round up division
    total_pages_publications = (total_publications + per_page - 1) // per_page

    # Render the HTML template and pass the data
    return render_template(
        'index.html',
        events=events,
        publications=publications,
        page_events=page_events,
        total_pages_events=total_pages_events,
        page_publications=page_publications,
        total_pages_publications=total_pages_publications,
        search=search,
        sort_events=sort_events,
        order_events=order_events,
        sort_publications=sort_publications,
        order_publications=order_publications
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

