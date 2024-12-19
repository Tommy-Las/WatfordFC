import pandas as pd
import numpy as np

"""
Load and prepare GPS data with proper date conversion.
"""
def load_and_prepare_data(data_path):
    
    try:
        
        # Import data
        df = pd.read_csv(data_path)
        
        # Create a copy to avoid modifying the original dataframe
        processed_df = df.copy()
        
        # Convert PlayerID to int
        processed_df['PlayerID'] = processed_df['PlayerID'].astype(int)
        
        # Convert date to datetime pandas object
        processed_df['DATE'] = pd.to_datetime(processed_df['DATE'])
        
        # Test data is being imported correcty
        print(f"Processed columns: {processed_df.columns.tolist()}")
        print(f"Number of rows: {len(processed_df)}")
        print(f"Sample of processed data:\n{processed_df.head()}")
        print(f"Data types:\n{processed_df.dtypes}")
        print(f"Unique player names: {processed_df['PlayerID'].unique()}")
        
        return processed_df
    
    except FileNotFoundError:
        print(f"File not found: {data_path}")
        raise FileNotFoundError(f"Data file not found at {data_path}")
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        raise Exception(f"Error processing data: {str(e)}")

def filter_data_by_date_range(df, start_date, end_date):
    """Filter dataframe by date range."""
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    dates = (df['DATE'] >= start_date) & (df['DATE'] <= end_date)
    return df[dates]

"""
Format date and microcycle in the desired format.
"""
def format_date_microcycle(date, microcycle):
    return f"{date.strftime('%Y %B %d')} - {microcycle}"
