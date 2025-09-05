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

This script calculates the number of each event type grouped by 
month and year, including handling multiple event types separated by commas.
It visualizes the trends over time using a line plot.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_event_types_over_time():
    """Analyze and visualize the number of each event type over time (month/year)"""
    
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
    
    # SQL query to retrieve event types and event dates
    query = """
    SELECT 
        event_type,
        strftime('%Y-%m', event_date) AS event_month_year
    FROM 
        events
    ORDER BY 
        event_month_year ASC;
    """
    
    try:
        # Execute the query and load results into a Pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Split comma-separated event types and expand the DataFrame
        expanded_rows = []
        for _, row in df.iterrows():
            event_types = [etype.strip() for etype in row['event_type'].split(',')]
            for event_type in event_types:
                expanded_rows.append({'event_type': event_type, 'event_month_year': row['event_month_year']})
        
        # Create a new DataFrame with expanded rows
        expanded_df = pd.DataFrame(expanded_rows)
        
        # Group by event_type and event_month_year, and count occurrences
        grouped_df = expanded_df.groupby(['event_type', 'event_month_year']).size().reset_index(name='event_count')
        
        # Convert event_month_year to a datetime object for better plotting
        grouped_df['event_month_year'] = pd.to_datetime(grouped_df['event_month_year'], format='%Y-%m')
        
        # Set up the visualization
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=grouped_df, x='event_month_year', y='event_count', hue='event_type', marker='o')
        
        # Customize the plot
        plt.title('Number of Each Event Type Over Time (Month/Year)', fontsize=16)
        plt.xlabel('Month/Year', fontsize=12)
        plt.ylabel('Number of Events', fontsize=12)
        plt.legend(title='Event Type', fontsize=10)
        plt.grid(True)
        plt.tight_layout()
        
        # Show the plot
        plt.show()
        
        print("\nVisualization generated successfully.")
    except sqlite3.Error as e:
        print(f"❌ Query execution error: {e}")
    finally:
        # Close the database connection
        conn.close()
        print("\n✓ Database connection closed.")

# Run the analysis
if __name__ == "__main__":
    analyze_event_types_over_time()

# ------------------------------------------------------------------------------------------------------------

#!/usr/bin/env python3
"""
Event Type and Location Analysis in Zines Database
History 8510 - Clemson University

This script calculates:
1. The number of each event type grouped by location (city, state, country).
2. The total number of events grouped by location.

It handles multiple event types separated by commas and orders the results from most to least frequent.
"""

import sqlite3
import pandas as pd

def analyze_event_types_and_totals_by_location():
    """Analyze the number of each event type and total events grouped by location"""
    
    print("=== Event Type and Location Analysis in Zines Database ===")
    print("History 8510 - Clemson University")
    print("=" * 60)
    
    # Connect to zines.db database
    try:
        conn = sqlite3.connect('zines.db')
        print("✓ Connected to Zines database (zines.db)")
    except sqlite3.Error as e:
        print(f"❌ Database connection error: {e}")
        return
    
    # SQL query to retrieve event types and locations
    query = """
    SELECT 
        event_type,
        city || ', ' || state || ', ' || country AS location
    FROM 
        events
    ORDER BY 
        location ASC;
    """
    
    try:
        # Execute the query and load results into a Pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Split comma-separated event types and expand the DataFrame
        expanded_rows = []
        for _, row in df.iterrows():
            event_types = [etype.strip() for etype in row['event_type'].split(',')]
            for event_type in event_types:
                expanded_rows.append({'event_type': event_type, 'location': row['location']})
        
        # Create a new DataFrame with expanded rows
        expanded_df = pd.DataFrame(expanded_rows)
        
        # Group by event_type and location, and count occurrences
        event_type_counts = expanded_df.groupby(['event_type', 'location']).size().reset_index(name='event_count')
        
        # Group by location only, and count total events
        total_event_counts = expanded_df.groupby(['location']).size().reset_index(name='total_event_count')
        
        # Sort both DataFrames by their counts in descending order
        event_type_counts = event_type_counts.sort_values(by='event_count', ascending=False)
        total_event_counts = total_event_counts.sort_values(by='total_event_count', ascending=False)
        
        # Display the results
        print("\nNumber of Each Event Type by Location (Ordered by Most to Least):")
        print(event_type_counts.to_string(index=False))
        
        print("\nTotal Number of Events by Location (Ordered by Most to Least):")
        print(total_event_counts.to_string(index=False))
    except sqlite3.Error as e:
        print(f"❌ Query execution error: {e}")
    finally:
        # Close the database connection
        conn.close()
        print("\n✓ Database connection closed.")

# Run the analysis
if __name__ == "__main__":
    analyze_event_types_and_totals_by_location()

# ---------------------------------------------------------------------------------------------------------

#!/usr/bin/env python3
"""
Event Advertisement and Protest Report Analysis in Berkeley and San Francisco
History 8510 - Clemson University

This script calculates the maximum number of Event Advertisement and Protest Report 
events in Berkeley and San Francisco for a given issue, grouped by volume and issue number,
and ordered by volume and issue number in ascending order.
"""

import sqlite3
import pandas as pd

def analyze_event_advertisements_and_protests():
    """Analyze Event Advertisement and Protest Report counts in Berkeley and San Francisco"""
    
    print("=== Event Advertisement and Protest Report Analysis ===")
    print("History 8510 - Clemson University")
    print("=" * 60)
    
    # Connect to zines.db database
    try:
        conn = sqlite3.connect('zines.db')
        print("✓ Connected to Zines database (zines.db)")
    except sqlite3.Error as e:
        print(f"❌ Database connection error: {e}")
        return
    
    # SQL query to join events and publications and calculate counts
    query = """
    SELECT 
        p.pub_title AS publication_title,
        p.volume AS volume_number,
        p.issue_number AS issue_number,
        e.city,
        COUNT(CASE WHEN e.event_type LIKE '%Event Advertisement%' THEN 1 END) AS event_advertisements_count,
        COUNT(CASE WHEN e.event_type LIKE '%Protest Report%' THEN 1 END) AS protest_reports_count,
        COUNT(*) AS total_events
    FROM 
        events e
    JOIN 
        publications p
    ON 
        e.publication_id = p.pub_id
    WHERE 
        e.city IN ('Berkeley', 'San Francisco')
        AND (e.event_type LIKE '%Event Advertisement%' OR e.event_type LIKE '%Protest Report%')
    GROUP BY 
        p.pub_title, p.volume, p.issue_number, e.city
    ORDER BY 
        p.volume ASC, p.issue_number ASC;
    """
    
    try:
        # Execute the query and load results into a Pandas DataFrame
        df = pd.read_sql_query(query, conn)
        
        print("\nMaximum Number of Event Advertisements and Protest Reports by Volume and Issue:")
        print(df.to_string(index=False))
    except sqlite3.Error as e:
        print(f"❌ Query execution error: {e}")
    finally:
        # Close the database connection
        conn.close()
        print("\n✓ Database connection closed.")

# Run the analysis
if __name__ == "__main__":
    analyze_event_advertisements_and_protests()