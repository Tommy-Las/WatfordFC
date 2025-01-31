import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

"""
Steps to take:

- Import both files
- Verify and change datatypes
- Merge both files
- Get list of players of last session and verify they have enough data to perform calculations

"""


def read_files():
    try:
        # Get the current directory
        current_dir = os.getcwd()

        # List all files in the current directory
        files = [f for f in os.listdir(current_dir) if os.path.isfile(f)]

        # Ensure there are at least two files in the folder
        if len(files) < 2:
            raise FileNotFoundError(
                "Not enough files in the folder! Ensure at least two files are present."
            )

        # Read Excel files
        df_gps = pd.read_excel("data/GPS 2018-2023_NoContact.xlsx")
        df_speed = pd.read_excel("data/max_speed.xlsx")

        return df_gps, df_speed

    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
        return None, None

    except Exception as e:
        print(f"An error occurred while reading the files: {e}")
        return None, None


def process_duplicates(df_gps, df_speed):
    df_speed = df_speed.groupby(["DATE", "ID"]).agg("max").reset_index()

    # Define columns to sum
    columns_to_sum = ["Total D", ">19.8", "> 25 Km/h", "ACC", "DEC"]

    # Define columns to select the first value
    columns_to_first = [
        "DATE",
        "Column2",
        "PLAYER",
        "Injury",
        "season",
        "LEAGUE",
        "preseason-season",
        "MANAGER",
    ]

    # Group by the duplicate subset and aggregate
    df_gps_aggregated = (
        df_gps[df_gps.duplicated(subset=["PLAYER", "DATE"], keep=False)]
        .groupby(["PLAYER", "DATE"], as_index=False)
        .agg(
            {
                **{col: "sum" for col in columns_to_sum},
                **{col: "first" for col in columns_to_first},
            }
        )
    )

    # Ensure non-duplicated rows are preserved by combining them back
    df_gps_combined = pd.concat(
        [
            df_gps[~df_gps.duplicated(subset=["PLAYER", "DATE"], keep=False)],
            df_gps_aggregated,
        ],
        ignore_index=True,
    )

    return df_gps_combined, df_speed


def process_and_merge_dfs(df_gps, df_speed):
    try:
        # Convert DATE column values into Pandas datetime object
        df_gps["DATE"] = pd.to_datetime(df_gps["DATE"], dayfirst=True)
        df_speed["DATE"] = pd.to_datetime(df_speed["DATE"], dayfirst=True)

        # Drop NULL values for 'PLAYER'
        df_gps = df_gps.dropna(subset=['PLAYER'])

        # Convert ID and PLAYER columns to the same data type - integers
        df_gps.loc[:, 'PLAYER'] = df_gps['PLAYER'].astype(int)
        df_speed.loc[:,'ID'] = df_speed['ID'].astype(int)

        # Get the latest date in the DATE column
        latest_date = df_gps["DATE"].max()
        
        # Calculate the start date (20 days before the latest date)
        start_date = latest_date - pd.Timedelta(days=20)

        # Filter the dataframe for rows between the start_date and latest_date (inclusive)
        df_gps_filtered = df_gps[(df_gps['DATE'] >= start_date) & (df_gps['DATE'] <= latest_date)]

        # Example merge operation
        merged_df = pd.merge(df_gps_filtered, df_speed, on="DATE", how="inner")

        # Perform an inner join on matching DATE and PLAYER/ID values
        merged_df = df_gps_filtered.merge(df_speed, left_on=['DATE', 'PLAYER'], right_on=['DATE', 'ID'], how='inner')

        merged_df.reset_index(drop=True, inplace=True)

        print("DataFrames processed and merged successfully.")
        
        return merged_df
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    except KeyError as key_error:
        print(
            f"KeyError: {key_error}. Check if the 'DATE' column exists in both DataFrames."
        )
        return None

    except Exception as e:
        print(f"An error occurred while processing and merging DataFrames: {e}")
        return None

def data_processing(df):
    cols = ['Total D', '>19.8', '> 25 Km/h', 'ACC',
       'DEC', 'ID', 'Max Speed', 'Sprints', 'MINUTES', 'Max Speed Season',
       'Avg Speed Season', '% Max Speed',
       '%Speed diference against max. Speed average']
    
    df[cols] = df[cols].astype(float)
    df.rename(columns=column_rename_dict, inplace=True)
    
    df = session_OHE(df)

    return df

def calcular_acumulado(df, columnas_calcular, dias):
    # Columns to exclude when the day is 3
    excluded_columns_3_days = ['TD_Rel', '>19.8_Rel', '>25_Rel', 'ACC_Rel', 'DEC_Rel', '% Max Speed']

    # Create an empty list to store processed player DataFrames
    processed_players = []

    # Process each player separately
    for player_id in df['PlayerID'].unique():
        # Filter data for the current player
        player_data = df[df['PlayerID'] == player_id].copy()

        # Create a full date range for the player (from the first to the last recorded date)
        full_date_range = pd.date_range(start=player_data['DATE'].min(), end=player_data['DATE'].max(), freq='D')

        # Set 'DATE' as the index and reindex to fill missing dates with zeros
        player_data = player_data.set_index('DATE').reindex(full_date_range, fill_value=0).reset_index()
        player_data.rename(columns={'index': 'DATE'}, inplace=True)
        player_data['PlayerID'] = player_id

        # Perform rolling calculations for each metric, excluding the current day
        for dia in dias:
            for col in columnas_calcular:
                # Skip excluded columns when the day is 3
                if dia != 1 and col in excluded_columns_3_days:
                    continue

                # Check if the column exists to avoid errors
                if col in player_data.columns:
                    if dia in [7, 21]:
                        # Rolling sum, mean, and std for 7 and 21 days
                        player_data[f'{col}-{dia}'] = (
                            player_data[col].rolling(window=dia, min_periods=1).sum()
                        )
                        player_data[f'{col}-{dia}-avg'] = (
                            player_data[col].rolling(window=dia, min_periods=1).mean()
                        )
                        player_data[f'{col}-{dia}-std'] = (
                            player_data[col].rolling(window=dia, min_periods=1).std()
                        )
                    else:
                        # Only rolling sum for other periods
                        player_data[f'{col}-{dia}'] = (
                            player_data[col].rolling(window=dia, min_periods=1).sum()
                        )

        # Drop rows where all calculated values are zero (rest days)
        mask_non_zero = (player_data[columnas_calcular].sum(axis=1) > 0)
        player_data = player_data[mask_non_zero]

        # Append the processed player's data to the list
        processed_players.append(player_data)

    # Concatenate all processed player DataFrames into a single DataFrame
    df_resultado = pd.concat(processed_players, ignore_index=True)

    return df_resultado

def filter_players(df):
    # Step 1: Select the rows with the latest date
    latest_date = df['DATE'].max()
    latest_date_rows = df[df['DATE'] == latest_date]

    # Step 2: Iterate through each row to check TD, TD-3, and TD7 values
    for index, row in latest_date_rows.iterrows():
        if row['TD'] == row['TD-3'] == row['TD-7']:
            # Print PlayerID and drop the row
            print(f"PlayerID {row['PlayerID']} does not have enough information.")
            df = df.drop(index)

    return df

def calculate_fatigue_metrics(df, metrics):
    min_threshold = 1e-5  # Small constant to replace zeros
    
    # Calculate ACWR, MSWR for each metric
    for metric in metrics:
        # Replace zeroes with min value to avoid division by 0
        df[f'{metric}-21-avg'] = df[f'{metric}-21-avg'].replace(0, min_threshold)
        df[f'{metric}-7-std'] = df[f'{metric}-7-std'].replace(0, min_threshold)

        # Calculate 7-day and 28-day averages for ACWR
        df[f'{metric}_ACWR'] = df[f'{metric}-7-avg'] / df[f'{metric}-21-avg']

        # Calculate mean and standard deviation for MSWR
        df[f'{metric}_MSWR'] = df[f'{metric}-7-avg'] / df[f'{metric}-7-std']

    cumulative_df.drop(columns=columns_to_drop , inplace=True)

    return df

def session_OHE(df):
    # Strip spaces
    df['Session'] = df['Session'].str.replace(' ', '', regex=False)
    
    # Replace ['MD', 'MD(HOME)', 'MD(AWAY)'] with 'MD'
    md_values = ['MD', 'MD(HOME)', 'MD(AWAY)']
    df['Session'] = df['Session'].replace(md_values, 'MD')

    # Perform one-hot encoding
    encoded_df = pd.get_dummies(df, columns=['Session'], prefix='Session')

    one_hot_columns = [col for col in encoded_df.columns if col.startswith('Session_')]
    encoded_df[one_hot_columns] = encoded_df[one_hot_columns].astype(int)

    #encoded_df = final_df.dropna(subset=one_hot_columns)
    return encoded_df

def process_data_testing(df):
    latest_date = df['DATE'].max()
    latest_date_rows = df[df['DATE'] == latest_date]

    columns_to_rename = ['TD', '>19.8', '>25', 'ACC', 'DEC', 'Sprints', 'Mins']

    # Rename columns by adding -1
    latest_date_rows.rename(columns={col: f"{col}-1" for col in columns_to_rename}, inplace=True)
    
    return latest_date_rows

cols_calculate_loads = ['TD', '>19.8', '>25', 'ACC', 'DEC', 'Sprints', '% Max Speed']


cols_calculate_fatigues= ['TD', '>19.8', '>25', 'ACC', 'DEC']

column_rename_dict = {
    'Column2': 'Session',
    'ID': 'PlayerID',
    'Total D': 'TD',
    '>19.8': '>19.8',
    '> 25 Km/h': '>25',
    '%Speed diference against max. Speed average': 'Speed Diff Max Avg',
    'Injury': 'Injury',
    'MINUTES': 'Mins',
}

columns_to_drop = ['TD-7-avg', 'TD-7-std',
    '>19.8-7-avg', '>19.8-7-std', '>25-7-avg',
       '>25-7-std', 'ACC-7-avg', 'ACC-7-std', 'DEC-7-avg',
       'DEC-7-std', 'Sprints-7-avg', 'Sprints-7-std', 'TD-21-avg', 'TD-21-std', '>19.8-21-avg', '>19.8-21-std', '>25-21-avg',
       '>25-21-std', 'ACC-21-avg', 'ACC-21-std',
       'DEC-21-avg', 'DEC-21-std', 'Sprints-21-avg','Sprints-21-std']

if __name__ == "__main__":
    # Call the function to process files in the current directory
    df_gps, df_speed = read_files()

    if df_gps is None or df_speed is None:
        print("File reading failed. Exiting program.")
        exit()

    # Process duplicates (placeholder function)
    df_gps, df_speed = process_duplicates(df_gps, df_speed)

    # Process and merge DataFrames
    merged_df = process_and_merge_dfs(df_gps, df_speed)
        
    merged_df = data_processing(merged_df)

    merged_df.info()

    cumulative_df = calcular_acumulado(merged_df, cols_calculate_loads, [3,7,21])
    
    # Filter players with enough data

    filtered_df = filter_players(cumulative_df)

    complete_df = calculate_fatigue_metrics(filtered_df,  cols_calculate_fatigues)

    test_df = process_data_testing(complete_df)

    metrics_train = ['TD-1', '>19.8-1', '>25-1', 'ACC-1', 'DEC-1', 'Sprints-1',
       'Mins-1', '% Max Speed-1', 'TD-3', '>19.8-3', '>25-3', 'ACC-3',
       'DEC-3', 'Sprints-3', 'TD-7', '>19.8-7', '>25-7', 'ACC-7',
       'DEC-7', 'Sprints-7', 'TD-21', '>19.8-21', '>25-21', 'ACC-21',
       'DEC-21', 'Sprints-21', 'TD_ACWR', 'TD_MSWR', '>19.8_ACWR',
       '>19.8_MSWR', '>25_ACWR', '>25_MSWR', 'ACC_ACWR', 'ACC_MSWR',
       'DEC_ACWR', 'DEC_MSWR','Session_M+1', 'Session_M+2', 'Session_M+3',
       'Session_M-1', 'Session_M-2', 'Session_M-3', 'Session_M-4',
       'Session_M-5', 'Session_MD']

    # Load the classifier
    model = joblib.load('xgb_classifier_model.pkl')

    # predictions = model.predict(X_test)  # Assuming X_test is your test data
    # print(predictions)

