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