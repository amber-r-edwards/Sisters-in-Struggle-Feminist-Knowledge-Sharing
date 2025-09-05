#!/usr/bin/env python3
"""
Event Type Analysis in Zines Database
History 8510 - Clemson University

This script answers the question: What is the total count of each event type 
across all publications in the zines.db database?

Handles events with multiple types (comma-separated) by splitting them and 
attributing each type to its respective total count.
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
    
    # SQL query to retrieve all event types
    query = """
    SELECT 
        event_type
    FROM 
        events
    """
    
    try:
        # Execute the query and load results into a Pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Split comma-separated event types and count each type
        event_counts = {}
        for event_type_list in df['event_type']:
            # Split the event_type string by commas and strip whitespace
            event_types = [etype.strip() for etype in event_type_list.split(',')]
            for event_type in event_types:
                if event_type in event_counts:
                    event_counts[event_type] += 1
                else:
                    event_counts[event_type] = 1
        
        # Convert the event_counts dictionary to a DataFrame for display
        result_df = pd.DataFrame(list(event_counts.items()), columns=['event_type', 'total_count'])
        result_df = result_df.sort_values(by='total_count', ascending=False)
        
        print("\nEvent Type Counts Across All Publications:")
        print(result_df.to_string(index=False))
    except sqlite3.Error as e:
        print(f"❌ Query execution error: {e}")
    finally:
        # Close the database connection
        conn.close()
        print("\n✓ Database connection closed.")

# Run the analysis
if __name__ == "__main__":
    analyze_event_types()

# ---------------------------------------------------------------------------------------------------------

#!/usr/bin/env python3
"""
Event Type and Date Analysis in Zines Database
History 8510 - Clemson University

This script calculates the average count of each event type grouped by 
month and year, and orders the results in descending order.
"""

import sqlite3
import pandas as pd

def analyze_event_types_by_date():
    """Analyze the average count of each event type grouped by month and year"""
    
    print("=== Event Type and Date Analysis in Zines Database ===")
    print("History 8510 - Clemson University")
    print("=" * 60)
    
    # Connect to zines.db database
    try:
        conn = sqlite3.connect('zines.db')
        print("✓ Connected to Zines database (zines.db)")
    except sqlite3.Error as e:
        print(f"❌ Database connection error: {e}")
        return
    
    # SQL query to calculate the average count of each event type by month and year
    query = """
    SELECT 
        event_type,
        strftime('%Y-%m', event_date) AS event_month_year,
        COUNT(*) * 1.0 / COUNT(DISTINCT strftime('%Y-%m', event_date)) AS avg_count
    FROM 
        events
    GROUP BY 
        event_type, event_month_year
    ORDER BY 
        avg_count DESC;
    """
    
    try:
        # Execute the query and load results into a Pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        print("\nAverage Count of Each Event Type by Month and Year (Ordered by Avg Count):")
        print(df.to_string(index=False))
    except sqlite3.Error as e:
        print(f"❌ Query execution error: {e}")
    finally:
        # Close the database connection
        conn.close()
        print("\n✓ Database connection closed.")

# Run the analysis
if __name__ == "__main__":
    analyze_event_types_by_date()
