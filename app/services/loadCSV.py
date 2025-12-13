import pandas as pd
import sys
import sqlite3
def load_csv_to_table(conn, csv_path, table_name: str) -> int:
    """
    Load a CSV file into a database table using pandas.
    
    """
    row_count = 0
    
    print(f"Attempting to load data from {csv_path} into table '{table_name}'...")
    
    try:
        
        # header = 0  assumes the first row of the CSV is the column names.
        df = pd.read_csv(csv_path, header=0)
        
        df.to_sql(
            name=table_name, 
            con=conn, 
            if_exists='append', 
            index=False
        )
        
        row_count = len(df)
        
        print(f"Success: Loaded {row_count} rows into table '{table_name}'.")
        return row_count
    
     
    # Flag different types of errros when loading csv files to ensure that the files are inserted correctly
          

    except FileNotFoundError:
        print(f"Error: CSV file not found at path: {csv_path}", file=sys.stderr)
    except pd.errors.EmptyDataError:
        print(f"Error: The CSV file {csv_path} is empty.", file=sys.stderr)
    except pd.errors.ParserError as e:
        print(f"Error: Could not parse CSV file. Details: {e}", file=sys.stderr)
    except sqlite3.Error as e:
        print(f"Database error during insertion: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        
    return 0