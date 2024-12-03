import pandas as pd
import numpy as np

def load_and_prepare_data(data_path):
    """Load and prepare GPS data with proper date conversion."""
    df = pd.read_csv(data_path)
    # Convert date to datetime for proper handling
    df['date'] = pd.to_datetime(df['date'])
    return df

def filter_data_by_date_range(df, start_date, end_date):
    """Filter dataframe by date range."""
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    return df[mask]

def get_player_id_by_name(df, player_name):
    """Get player ID from player name."""
    return df[df['player_name'] == player_name]['player_id'].iloc[0]

def get_date_range_bounds(df):
    """Get the minimum and maximum dates from the dataset."""
    return df['date'].min(), df['date'].max()