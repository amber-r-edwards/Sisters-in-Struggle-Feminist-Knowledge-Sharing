# Amber Edwards
# Sept 11 2025
# Importing CSV Data into Database
# existing CSV of data from It Ain't Me Babe

import sqlite3
import csv

# File paths for the database and CSV files
database_file = 'zines.db'
publications_csv = 'babepubs.csv'
events_csv = 'babeevents.csv'

print("=== Importing Data into zines.db ===")

# Step 1: Connect to the SQLite database
print("\nStep 1: Connecting to zines.db...")
conn = sqlite3.connect(database_file)
cursor = conn.cursor()
print("✓ Connected to zines.db")

# Step 2: Import data into the publications table
print("\nStep 2: Importing data into the publications table...")
try:
    with open(publications_csv, 'r') as file:
        reader = csv.DictReader(file)  # Use DictReader to map column names
        for row in reader:
            # Combine year, month, and day into a single date string (YYYY-MM-DD)
            issue_date = f"{row['issue_year']}-{row['issue_month'].zfill(2)}-{row['issue_day'].zfill(2)}"
            cursor.execute('''
                INSERT INTO publications (pub_title, volume, issue_number, issue_date, volume_title, author_org, location)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['pub_title'], 
                row['volume'], 
                row['issue_number'], 
                issue_date, 
                row['volume_title'], 
                row['author_org'], 
                row['location']
            ))
    print("✓ Imported data into the publications table")
except Exception as e:
    print(f"Error importing data into publications table: {e}")

# Step 3: Import data into the events table
print("\nStep 3: Importing data into the events table...")
try:
    with open(events_csv, 'r') as file:
        reader = csv.DictReader(file)  # Use DictReader to map column names
        for row in reader:
            # Combine year, month, and day into a single date string (YYYY-MM-DD)
            event_date = f"{row['event_year']}-{row['event_month'].zfill(2)}-{row['event_date'].zfill(2)}"

            # Look up the publication_id in the publications table using volume and issue_number
            cursor.execute('''
                SELECT pub_id FROM publications
                WHERE volume = ? AND issue_number = ?
            ''', (row['volume'], row['issue_number']))
            result = cursor.fetchone()

            if result:
                publication_id = result[0]  # Extract the pub_id from the query result
                # Insert the event into the events table
                cursor.execute('''
                    INSERT INTO events (publication_id, event_title, event_type, event_date, location, address, city, state, country, description, source_publication)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (publication_id, row['event_title'], row['event_type'], event_date, row['location'], row['address'], row['city'], row['state'], row['country'], row['description'], row['source_publication']))
            else:
                print(f"Warning: No matching publication found for event: {row['event_title']} (Volume: {row['volume']}, Issue: {row['issue_number']})")
    print("✓ Data imported into events table")
except Exception as e:
    print(f"Error importing data into events table: {e}")

# Step 4: Commit changes and close the connection
print("\nStep 4: Saving changes and closing the database connection...")
conn.commit()
conn.close()
print("✓ Data imported successfully!")