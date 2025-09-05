#!/usr/bin/env python3
"""
Event Type Analysis in Zines Database
History 8510 - Clemson University

This script answers the question: What is the total count of each event type 
across all publications in the zines.db database?

Uses a simple SQL query to analyze event type distribution.
"""

import sqlite3
import pandas as pd

def analyze_event_types():
    """Analyze the total count of each event type across all publications"""
    
    print("=== Event Type Analysis in Zines Database ===")
    print("History 8510 - Clemson University")
    print("=" * 60)
    
    # Connect to zines.db database
    try:
        conn = sqlite3.connect('zines.db')
        print("✓ Connected to Zines database (zines.db)")
    except sqlite3.Error as e:
        print(f"❌ Database connection error: {e}")
        return
    
    # SQL query to count event types
    query = """
    SELECT 
        event_type,
        COUNT(event_type) AS total_count
    FROM 
        events
    GROUP BY 
        event_type
    ORDER BY 
        total_count DESC;
    """
    
    try:
        # Execute the query and load results into a Pandas DataFrame
        df = pd.read_sql_query(query, conn)
        print("\nEvent Type Counts Across All Publications:")
        print(df.to_string(index=False))
    except sqlite3.Error as e:
        print(f"❌ Query execution error: {e}")
    finally:
        # Close the database connection
        conn.close()
        print("\n✓ Database connection closed.")

# Run the analysis
if __name__ == "__main__":
    analyze_event_types()