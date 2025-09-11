import sqlite3
import csv

# Path to the SQLite database
DB_PATH = 'zines.db'

# Path to the CSV file
CSV_PATH = 'baberesources.csv'

def recreate_resources_table():
    """
    Delete the 'resources' table if it exists and recreate it with the specified columns.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop the 'resources' table if it exists
    cursor.execute('DROP TABLE IF EXISTS resources')

    # Create the 'resources' table with the specified columns
    cursor.execute('''
        CREATE TABLE resources (
            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_title TEXT,
            volume INTEGER,
            issue INTEGER,
            resource_type TEXT,
            location TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            country TEXT,
            source_publication TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Table 'resources' recreated successfully.")

def import_csv_to_resources():
    """
    Import data from the CSV file into the 'resources' table.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Open the CSV file and insert data into the 'resources' table
    with open(CSV_PATH, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('''
                INSERT INTO resources (resource_title, volume, issue, resource_type, location, address, city, state, country, source_publication, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row.get('resource_title', 'NA'),
                row.get('volume', None),
                row.get('issue', None),
                row.get('resource_type', 'NA'),
                row.get('location', 'NA'),
                row.get('address', 'NA'),
                row.get('city', 'NA'),
                row.get('state', 'NA'),
                row.get('country', 'NA'),
                row.get('source_publication', 'NA'),
                row.get('description', 'NA')
            ))
    
    conn.commit()
    conn.close()
    print("Data imported into 'resources' table successfully.")

def move_courses_to_events():
    """
    Extract rows with resource_type 'Courses' from the 'resources' table
    and move them into the 'events' table, filling missing columns with 'NA' or 'NA-NA-NA'.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Select rows with resource_type 'Courses' and join with publications
    cursor.execute('''
        SELECT r.resource_title, r.description, r.city, r.state, r.country, r.resource_type, p.pub_id
        FROM resources r
        LEFT JOIN publications p
        ON r.volume = p.volume AND r.issue = p.issue_number
        WHERE r.resource_type = 'Courses'
    ''')
    courses = cursor.fetchall()

    # Move each row into the 'events' table
    for course in courses:
        resource_title = course[0] or 'NA'
        description = course[1] or 'NA'
        city = course[2] or 'NA'
        state = course[3] or 'NA'
        country = course[4] or 'NA'
        event_type = course[5] or 'NA'
        publication_id = course[6]  # This will be NULL if no match is found
        event_date = 'NA-NA-NA'  # Default date

        cursor.execute('''
            INSERT INTO events (event_title, description, publication_id, event_date, city, state, country, event_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (resource_title, description, publication_id, event_date, city, state, country, event_type))
    
    # Delete the moved rows from the 'resources' table
    cursor.execute('''
        DELETE FROM resources
        WHERE resource_type = 'Courses'
    ''')

    conn.commit()
    conn.close()
    print("Courses moved to 'events' table successfully.")

if __name__ == '__main__':
    recreate_resources_table()
    import_csv_to_resources()
    move_courses_to_events()