#import sqlite3
#import csv

# Path to the SQLite database
#DB_PATH = 'zines.db'

# Path to the CSV file
#CSV_PATH = 'baberesources.csv'

#def recreate_resources_table():
#    """
#    Delete the 'resources' table if it exists and recreate it with the specified columns.
#    """
#    conn = sqlite3.connect(DB_PATH)
#    cursor = conn.cursor()

    # Drop the 'resources' table if it exists
#    cursor.execute('DROP TABLE IF EXISTS resources')

    # Create the 'resources' table with the specified columns
#    cursor.execute('''
#        CREATE TABLE resources (
#            resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
#            resource_title TEXT,
#            volume INTEGER,
#            issue INTEGER,
#            resource_type TEXT,
#            location TEXT,
#            address TEXT,
#            city TEXT,
#            state TEXT,
#            country TEXT,
#            source_publication TEXT,
#            description TEXT
#        )
#    ''')
#    conn.commit()
#    conn.close()
#    print("Table 'resources' recreated successfully.")

#def import_csv_to_resources():
#    """
#    Import data from the CSV file into the 'resources' table.
#    Handles multiple resource types by splitting them into separate rows.
#    """
#    conn = sqlite3.connect(DB_PATH)
#    cursor = conn.cursor()

    # Open the CSV file and insert data into the 'resources' table
#    with open(CSV_PATH, 'r') as csvfile:
#        reader = csv.DictReader(csvfile)
#        for row in reader:
#            # Split the resource_type column into multiple types (assuming comma-separated)
#            resource_types = row.get('resource_type', 'NA').split(',')
#
#            for resource_type in resource_types:
#                resource_type = resource_type.strip()  # Remove extra spaces
#                cursor.execute('''
#                    INSERT INTO resources (resource_title, volume, issue, resource_type, location, address, city, state, country, source_publication, description)
#                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                ''', (
#                    row.get('resource_title', 'NA'),
#                    row.get('volume', None),
#                    row.get('issue', None),
#                    resource_type,
#                    row.get('location', 'NA'),
#                    row.get('address', 'NA'),
#                    row.get('city', 'NA'),
#                    row.get('state', 'NA'),
#                    row.get('source_publication', 'NA'),
#                    row.get('description', 'NA')
#                ))
    
#    conn.commit()
#    conn.close()
#    print("Data imported into 'resources' table successfully.")

#def move_courses_to_events():
#    """
#    Move all rows with resource_type 'Courses' from the 'resources' table
#    into the 'events' table, matching columns directly.
#    """
#    conn = sqlite3.connect(DB_PATH)
#    cursor = conn.cursor()

    # Insert rows with resource_type 'Courses' into the events table
#    cursor.execute('''
#        INSERT INTO events (event_title, description, publication_id, event_date, city, state, country, event_type, location, address, source_publication)
#        SELECT r.resource_title, r.description, p.pub_id, NULL, r.city, r.state, r.country, r.resource_type, r.location, r.address, r.source_publication
#        FROM resources r
#        LEFT JOIN publications p
#       ON r.volume = p.volume AND r.issue = p.issue_number
#        WHERE r.resource_type = 'Courses'
#    ''')

    # Delete the moved rows from the resources table
#    cursor.execute('''
#        DELETE FROM resources
#        WHERE resource_type = 'Courses'
#    ''')

#    conn.commit()
#    conn.close()
#    print("Courses moved to 'events' table successfully.")

#if __name__ == '__main__':
#    recreate_resources_table()
#    import_csv_to_resources()
#    move_courses_to_events()

# fix to NULL values still sitting in events table
#-----------------------------------------------------------------------------------------

#import sqlite3

# Path to the SQLite database
#DB_PATH = 'zines.db'

#def delete_events():
#    """
#    Delete rows with event_id between 235 and 288 (inclusive) from the 'events' table.
#    """
#    conn = sqlite3.connect(DB_PATH)
#    cursor = conn.cursor()

#    try:
        # Delete rows with event_id between 235 and 288
#        cursor.execute('''
#            DELETE FROM events
#            WHERE event_id BETWEEN 235 AND 288
#        ''')
#        conn.commit()
#        print("Events with event_id between 235 and 288 have been deleted successfully.")
#    except sqlite3.Error as e:
#        print(f"Error while deleting events: {e}")
#    finally:
#        conn.close()

#if __name__ == '__main__':
#    delete_events()

# ---------------------------------------------------------------------------------------
import sqlite3

# Path to the SQLite database
DB_PATH = 'zines.db'

def move_organizations_to_events():
    """
    Move rows with resource_type 'Organization' from the 'resources' table
    into the 'events' table, setting event_type to 'Meeting Advertisement'.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Insert rows with resource_type 'Organization' into the events table
        cursor.execute('''
            INSERT INTO events (event_title, description, publication_id, event_date, city, state, country, event_type, location, address, source_publication)
            SELECT 
                r.resource_title, 
                r.description, 
                p.pub_id, 
                NULL,  -- No event_date provided
                r.city, 
                r.state, 
                r.country, 
                'Meeting Advertisement',  -- Set event_type to 'Meeting Advertisement'
                r.location, 
                r.address, 
                r.source_publication
            FROM resources r
            LEFT JOIN publications p
            ON r.volume = p.volume AND r.issue = p.issue_number
            WHERE r.resource_type = 'Organization'
        ''')

        # Delete the moved rows from the resources table
        cursor.execute('''
            DELETE FROM resources
            WHERE resource_type = 'Organization'
        ''')

        conn.commit()
        print("Organizations moved to 'events' table successfully as 'Meeting Advertisement'.")
    except sqlite3.Error as e:
        print(f"❌ Error while moving organizations to events: {e}")
    finally:
        conn.close()
        print("\n✓ Database connection closed.")

# Run the function
if __name__ == "__main__":
    move_organizations_to_events()