#import sqlite3

# Path to the SQLite database
#DB_PATH = 'zines.db'

#def update_event_type():
#    """
#    Update all entries in the events table where event_type is 'Advocacy'
#    and change it to 'Direct Advocacy'.
#    """
#    try:
#        # Connect to the database
#        conn = sqlite3.connect(DB_PATH)
#        cursor = conn.cursor()
#
#        # Execute the update query
#        cursor.execute('''
#            UPDATE events
#            SET event_type = 'Direct Advocacy'
#            WHERE event_type = 'Advocacy';
#        ''')
#
#        # Commit the changes and close the connection
#        conn.commit()
#        print("Successfully updated event_type from 'Advocacy' to 'Direct Advocacy'.")
#    except Exception as e:
#        print(f"An error occurred: {e}")
#    finally:
#        conn.close()

# Run the function
#if __name__ == '__main__':
#    update_event_type()

# ------------------delete any duplicates-----------------------

#import sqlite3

# Path to the SQLite database
#DB_PATH = 'zines.db'

#def delete_duplicate_events():
#    """
#    Delete duplicate rows in the 'events' table, keeping only one copy of each duplicate.
#    Duplicates are determined by all columns except 'event_id'.
#    """
#    conn = sqlite3.connect(DB_PATH)
#    cursor = conn.cursor()

#    try:
        # Delete duplicates while keeping the row with the smallest event_id
#        cursor.execute('''
#            DELETE FROM events
#            WHERE event_id NOT IN (
#                SELECT MIN(event_id)
#                FROM events
#                GROUP BY event_title, description, publication_id, event_date, city, state, country, event_type, location, address, source_publication
#            )
#        ''')
#        conn.commit()
#        print("Duplicate rows in the 'events' table have been deleted successfully.")
#    except sqlite3.Error as e:
#        print(f"Error while deleting duplicates: {e}")
#    finally:
#        conn.close()

#if __name__ == '__main__':
#    delete_duplicate_events()

# -------- delete NULL rows--------
import sqlite3

# Path to the SQLite database
DB_PATH = 'zines.db'

def delete_events():
    """
    Delete rows with event_id between 289 and 405 (inclusive) from the 'events' table.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Delete rows with event_id between 289 and 405
        cursor.execute('''
            DELETE FROM events
            WHERE event_id BETWEEN 289 AND 405
        ''')
        conn.commit()
        print("Events with event_id between 289 and 405 have been deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error while deleting events: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    delete_events()