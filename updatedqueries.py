#!/usr/bin/env python3
"""
Join Publications with Events in Zines Database
History 8510 - Clemson University

This script retrieves events and their associated publications, including volume and issue numbers,
and filters rows where source_publication is not "NA".
"""

import sqlite3
import pandas as pd

def analyze_publications_and_events():
    """Analyze publications and events with valid source publications"""
    
    print("=== Publications and Events Analysis ===")
    print("History 8510 - Clemson University")
    print("=" * 60)
    # Connect to zines.db database
    try:
        conn = sqlite3.connect('zines.db')
        print("✓ Connected to Zines database (zines.db)")
    except sqlite3.Error as e:
        print(f"❌ Database connection error: {e}")
        return
    
    # SQL query to join publications and events, including volume and issue numbers
    query = """
    SELECT 
        e.event_title AS event_title,
        e.event_type AS event_type,
        e.event_date AS event_date,
        e.source_publication AS source_publication,
        p.volume AS volume_number,
        p.issue_number AS issue_number
    FROM 
        events e
    JOIN 
        publications p
    ON 
        e.publication_id = p.pub_id
    WHERE 
        e.source_publication IS NOT NULL
        AND e.source_publication != 'NA';
    """
    
    try:
        # Execute the query and load results into a Pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Display the data in a readable format
        print("\nPublications and Events (Filtered by Valid Source Publications):")
        print(df.to_string(index=False))
    except sqlite3.Error as e:
        print(f"❌ Query execution error: {e}")
    finally:
        # Close the database connection
        conn.close()
        print("\n✓ Database connection closed.")

# Run the analysis
if __name__ == "__main__":
    analyze_publications_and_events()