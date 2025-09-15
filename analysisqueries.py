import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# filepath: /Users/amberedwards/Library/CloudStorage/OneDrive-ClemsonUniversity/FA2025/8510/DatabaseProject/analysisquery.py
def analyze_publications_and_events():
    """Analyze publications and events with valid source publications and output results as a PNG table."""
    
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
    FROM events e
    LEFT JOIN publications p
    ON e.publication_id = p.pub_id
    WHERE e.source_publication IS NOT NULL AND e.source_publication != 'NA'
    ORDER BY e.event_date
    """
    
    try:
        # Execute the query and load the results into a DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Check if the DataFrame is empty
        if df.empty:
            print("No results found for the query.")
            return
        
        # Display the data in the console
        print("\nPublications and Events (Filtered by Valid Source Publications):")
        print(df.to_string(index=False))
        
        # Create a PNG table from the DataFrame
        fig, ax = plt.subplots(figsize=(12, len(df) * 0.5))  # Adjust height based on number of rows
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(df.columns))))  # Adjust column widths
        
        # Save the table as a PNG file
        output_path = "publications_and_events_table.png"
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        print(f"\n✓ Table saved as PNG: {output_path}")
    except sqlite3.Error as e:
        print(f"❌ Query execution error: {e}")
    finally:
        # Close the database connection
        conn.close()
        print("\n✓ Database connection closed.")

# Run the analysis
if __name__ == "__main__":
    analyze_publications_and_events()

#-----------------------------------------------------------------------------------------------
import sqlite3

# Path to the SQLite database
DB_PATH = 'zines.db'

def calculate_source_publication_ratio():
    """
    Calculate the ratio of events where source_publication is not 'NA' to the total number of events.
    Output the result as both a number and a percentage.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Query to count events where source_publication is not 'NA'
        cursor.execute('''
            SELECT COUNT(*) 
            FROM events
            WHERE source_publication IS NOT NULL AND source_publication != 'NA'
        ''')
        events_with_source = cursor.fetchone()[0]

        # Query to count total events
        cursor.execute('''
            SELECT COUNT(*) 
            FROM events
        ''')
        total_events = cursor.fetchone()[0]

        # Calculate the ratio and percentage
        if total_events > 0:
            ratio = events_with_source / total_events
            percentage = ratio * 100
        else:
            ratio = 0
            percentage = 0

        # Output the results
        print("=== Source Publication Ratio Analysis ===")
        print(f"Total Events: {total_events}")
        print(f"Events with Source Publication (not 'NA'): {events_with_source}")
        print(f"Ratio: {events_with_source}/{total_events} ({percentage:.2f}%)")
    except sqlite3.Error as e:
        print(f"❌ Query execution error: {e}")
    finally:
        # Close the database connection
        conn.close()
        print("\n✓ Database connection closed.")

# Run the analysis
if __name__ == "__main__":
    calculate_source_publication_ratio()

#92/308 - 29.87%
