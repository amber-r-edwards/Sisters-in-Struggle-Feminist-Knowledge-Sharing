# Amber Edwards
# Sept 11, 2025
# Creating the Database Structure
# database - publications table - events table

import sqlite3
import os

print("=== Creating Zines Database Structure ===")

# Step 1: Delete the existing database file (if it exists)
db_path = 'zines.db'
if os.path.exists(db_path):
    print("\nStep 1: Deleting existing zines.db...")
    os.remove(db_path)
    print("✓ Deleted existing zines.db")
else:
    print("\nStep 1: No existing zines.db found, skipping deletion.")

# Step 2: Connect to zines.db (creates file if it doesn't exist)
print("\nStep 2: Connecting to zines.db...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print("✓ Connected to zines.db")

# Step 3: Create publications table with updated schema
print("\nStep 3: Creating publications table...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS publications (
    pub_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique ID for each publication
    pub_title TEXT NOT NULL,                 -- Title of the publication
    volume INTEGER NOT NULL,                 -- Volume number
    issue_number INTEGER NOT NULL,           -- Issue number within the volume
    issue_date DATE,                         -- Full issue date (year, month, day)
    volume_title TEXT,                       -- Title of the volume (if applicable)
    author_org TEXT,                         -- Author or organization responsible for the publication
    location TEXT                            -- Location associated with the publication
)
''')
print("✓ Created publications table with updated schema")

# Step 4: Create events table
print("\nStep 4: Creating events table...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique ID for each event
    event_title TEXT NOT NULL,                  -- Title of the event
    event_date DATE,                            -- Date of the event
    description TEXT,                           -- Description of the event
    city TEXT,                                  -- City where the event occurred
    state TEXT,                                 -- State where the event occurred
    country TEXT,                               -- Country where the event occurred
    location TEXT,                              -- Specific location of the event (e.g., venue name)
    address TEXT,                               -- Street address of the event
    event_type TEXT,                            -- Type of event (e.g., conference, workshop)
    publication_id INTEGER,                     -- Foreign key to publications table
    source_publication TEXT,                    -- Source publication for the event if reprinted
    FOREIGN KEY (publication_id) REFERENCES publications (pub_id)
)
''')
print("✓ Created events table with all columns")

# Step 5: Commit changes and close the connection
print("\nStep 5: Saving changes and closing the database connection...")
conn.commit()
conn.close()
print("✓ Database structure created successfully!")