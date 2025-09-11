import sqlite3

# Path to the SQLite database
DB_PATH = 'zines.db'

def update_event_type():
    """
    Update all entries in the events table where event_type is 'Advocacy'
    and change it to 'Direct Advocacy'.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Execute the update query
        cursor.execute('''
            UPDATE events
            SET event_type = 'Direct Advocacy'
            WHERE event_type = 'Advocacy';
        ''')

        # Commit the changes and close the connection
        conn.commit()
        print("Successfully updated event_type from 'Advocacy' to 'Direct Advocacy'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Run the function
if __name__ == '__main__':
    update_event_type()