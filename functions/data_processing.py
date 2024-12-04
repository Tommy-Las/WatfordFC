import pandas as pd
import numpy as np

def load_and_prepare_data(data_path):
    """Load and prepare GPS data with proper date conversion."""
    try:
        print(f"Attempting to load data from: {data_path}")
        
        # Read CSV and ensure PlayerID is string
        df = pd.read_csv(data_path)
        
        # Create a copy to avoid modifying the original dataframe
        processed_df = df.copy()
        
        # Convert PlayerID to string and remove any decimal points
        processed_df['PlayerID'] = processed_df['PlayerID'].astype(int)
        
        # Convert date to datetime
        processed_df['DATE'] = pd.to_datetime(processed_df['DATE'])
        
        # Rename columns to match our application's naming convention
        column_mapping = {
            'PlayerID': 'player_name',  # PlayerID will be used as player_name
            'DATE': 'date',
            'Microcycle': 'microcycle',
            'TD': 'distance',
            'TD_Rel': 'relative_distance',
            'ACC': 'max_acceleration',
            'ACC_Rel': 'relative_acceleration',
            'DEC': 'max_deceleration',
            'DEC_Rel': 'relative_deceleration',
            'Sprints': 'total_sprints',
            'Mins': 'minutes',
            'Max Speed': 'max_speed',
            'Max Speed Season': 'season_max_speed',
            'Avg Speed Season': 'avg_speed',
            '% Max Speed': 'relative_max_speed',
            'Sprints_Rel': 'xxxx'
        }
        
        # Only rename columns that exist in the DataFrame
        existing_columns = {k: v for k, v in column_mapping.items() if k in processed_df.columns}
        processed_df = processed_df.rename(columns=existing_columns)
        
        # Debug prints
        print(f"Processed columns: {processed_df.columns.tolist()}")
        print(f"Number of rows: {len(processed_df)}")
        print(f"Sample of processed data:\n{processed_df.head()}")
        print(f"Data types:\n{processed_df.dtypes}")
        print(f"Unique player names: {processed_df['player_name'].unique()}")
        
        # Verify critical columns exist
        critical_columns = ['player_name', 'date', 'microcycle']
        missing_columns = [col for col in critical_columns if col not in processed_df.columns]
        if missing_columns:
            raise ValueError(f"Missing critical columns: {missing_columns}")
        
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
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    return df[mask]

def get_player_id_by_name(df, player_name):
    """Get player name (used as ID) from player name."""
    return str(player_name)  # Ensure player_name is string

def get_date_range_bounds(df):
    """Get the minimum and maximum dates from the dataset."""
    return df['date'].min(), df['date'].max()