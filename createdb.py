# Amber Edwards
# Aug 26, 2025
# Creating the Database Structure
# database - publications table - events table

import sqlite3

print("=== Creating Zines Database Structure ===")

# Step 1: Connect to zines.db (creates file if it doesn't exist)
print("\nStep 1: Connecting to zines.db...")
conn = sqlite3.connect('zines.db')
cursor = conn.cursor()
print("✓ Connected to zines.db")

# Step 2: Create publications table
print("\nStep 2: Creating publications table...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS publications (
    pub_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique ID for each publication
    pub_title TEXT NOT NULL,                 -- Title of the publication
    volume INTEGER NOT NULL,                 -- Volume number
    issue_number INTEGER NOT NULL,           -- Issue number within the volume
    issue_date DATE,                         -- Full issue date (year, month, day)
    volume_title TEXT                        -- Title of the volume (if applicable)
)
''')
print("✓ Created publications table")

# Step 3: Create events table
print("\nStep 3: Creating events table...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique ID for each event
    publication_id INTEGER NOT NULL,           -- Foreign key linking to publications
    event_title TEXT NOT NULL,                 -- Title of the event
    event_type TEXT,                           -- Type of the event (e.g., conference, workshop)
    event_date DATE,                           -- Date of the event
    location TEXT,                             -- Name of the venue or location
    address TEXT,                              -- Address of the event location
    city TEXT,                                 -- City where the event is held
    state TEXT,                                -- State or region where the event is held
    country TEXT,                              -- Country where the event is held
    description TEXT,                          -- Detailed description of the event
    source_publication TEXT,                   -- Source publication for the event
    FOREIGN KEY (publication_id) REFERENCES publications (pub_id) ON DELETE CASCADE
)
''')
print("✓ Created events table")

# Step 4: Commit changes and close the connection
print("\nStep 4: Closing connection to zines.db...")
conn.commit()
conn.close()
print("✓ zines.db structure created successfully")