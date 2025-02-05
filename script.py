import os
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import re

"""
Steps to take:

- Import both files
- Verify and change datatypes
- Merge both files
- Get list of players of last session and verify they have enough data to perform calculations

"""
selected_cols = [
    "Column1",
    "injury",
    "MD",
    "Session Date",
    "Total Time",
    "Total Distance",
    "Distance Zone 5 (Absolute)",
    "Distance Zone 6 (Absolute)",
    "Sprints",
    "% Max Speed",
    "ACC B1-3",
    "DEC B1-3",
]

rename_map = {
    "Column1": "PlayerID",
    "injury": "Injury",
    "MD": "Session",
    "Session Date": "Date",
    "Total Time": "Mins",
    "Total Distance": "TD",
    "Distance Zone 5 (Absolute)": ">19.8",
    "Distance Zone 6 (Absolute)": ">25",
    "Sprints": "Sprints",
    "% Max Speed": "% Max Speed",
    "ACC B1-3": "ACC",
    "DEC B1-3": "DEC",
}

cols_float = [
    "Total Time",
    "Total Distance",
    "Distance Zone 5 (Absolute)",
    "Distance Zone 6 (Absolute)",
    "Sprints",
    "% Max Speed",
    "ACC B1-3",
    "DEC B1-3",
]

cols_calculate_loads = ["TD", ">19.8", ">25", "ACC", "DEC", "Sprints", "% Max Speed"]

cols_calculate_fatigues = ["TD", ">19.8", ">25", "ACC", "DEC"]

columns_to_drop = [
    "TD-7-avg",
    "TD-7-std",
    ">19.8-7-avg",
    ">19.8-7-std",
    ">25-7-avg",
    ">25-7-std",
    "ACC-7-avg",
    "ACC-7-std",
    "DEC-7-avg",
    "DEC-7-std",
    "Sprints-7-avg",
    "Sprints-7-std",
    "TD-21-avg",
    "TD-21-std",
    ">19.8-21-avg",
    ">19.8-21-std",
    ">25-21-avg",
    ">25-21-std",
    "ACC-21-avg",
    "ACC-21-std",
    "DEC-21-avg",
    "DEC-21-std",
    "Sprints-21-avg",
    "Sprints-21-std",
]

def read_files():
    try:
        # Get the current directory
        current_dir = os.getcwd()

        # List all files in the current directory
        files = [f for f in os.listdir(current_dir) if os.path.isfile(f)]

        # Ensure there are at least two files in the folder
        if len(files) < 1:
            raise FileNotFoundError(
                "Not enough files in the folder! Ensure the file is present."
            )

        # Read Excel file
        df = pd.read_excel("Base De Datos 2024-25 SDC.xlsx")

        return df

    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
        return None, None

    except Exception as e:
        print(f"An error occurred while reading the files: {e}")
        return None, None


def process_duplicates(df):
    # Define columns to sum
    columns_to_sum = ["Injury", "Mins", "TD", ">19.8", ">25", "Sprints", "ACC", "DEC"]

    # Define columns to select the first value
    columns_to_first = ["PlayerID", "Session", "Date"]

    # Define columns to select the maximum value
    columns_to_max = ["% Max Speed"]

    # Print the duplicate rows
    duplicates = df[df.duplicated(subset=["PlayerID", "Date"], keep=False)]
    # print("Duplicates before processing:")
    # print(duplicates)

    # Function to set MD logic
    def set_md_logic(values):
        if "MD" in values.values:
            return "MD"
        values.values[0]

    # Group by the duplicate subset and aggregate
    df_aggregated = duplicates.groupby(["PlayerID", "Date"], as_index=False).agg(
        {
            **{col: "sum" for col in columns_to_sum},
            **{col: "first" for col in columns_to_first},
            **{col: "max" for col in columns_to_max},
            "Session": set_md_logic,  # Custom logic for MD column
        }
    )

    # Ensure non-duplicated rows are preserved by combining them back
    final_df = pd.concat(
        [df[~df.duplicated(subset=["PlayerID", "Date"], keep=False)], df_aggregated],
        ignore_index=True,
    )

    return final_df

def clean_session_value(session):
    # Check for the pattern +X/-X and extract the -X part
    match = re.search(r"(-\d+)", session)
    if match:
        return f"MD{match.group(1)}"  # Return MD concatenated with the negative value
    return session  # Return the original value if no -X is found


def data_processing(df):
    df = df[selected_cols]

    df.loc[: , cols_float] = df.loc[:, cols_float].astype(float)
    df = df.rename(columns=rename_map)


    df.loc[:,"Date"] = pd.to_datetime(df.loc[:,"Date"], dayfirst=True)

    # Select latest day and last days
    # df = df.groupby("PlayerID", group_keys=False).apply(
    #     lambda group: group[
    #         group["Date"] >= (group["Date"].max() - pd.Timedelta(days=20))
    #     ]
    # )

    # Target date and past 20 days
    target_date = pd.Timestamp('2025-01-20')
    date_range_start = target_date - pd.Timedelta(days=20)

    df = df.groupby("PlayerID", group_keys=False).apply(
    lambda group: group[
        (group["Date"] >= date_range_start) & (group["Date"] <= target_date)
    ]
    )

    # Example usage on a DataFrame column
    df["Session"] = df["Session"].apply(clean_session_value)

    df = process_duplicates(df)
    # df = session_OHE(df)

    return df


def calcular_acumulado(df, columnas_calcular, dias):
    # Columns to exclude when the day is 3
    excluded_columns_3_days = [
        "TD_Rel",
        ">19.8_Rel",
        ">25_Rel",
        "ACC_Rel",
        "DEC_Rel",
        "% Max Speed",
    ]

    # Create an empty list to store processed player DataFrames
    processed_players = []

    # Process each player separately
    for player_id in df["PlayerID"].unique():
        # Filter data for the current player
        player_data = df[df["PlayerID"] == player_id].copy()

        # Create a full date range for the player (from the first to the last recorded date)
        full_date_range = pd.date_range(
            start=player_data["Date"].min(), end=player_data["Date"].max(), freq="D"
        )

        # Set 'date' as the index and reindex to fill missing dates with zeros
        player_data = (
            player_data.set_index("Date")
            .reindex(full_date_range, fill_value=0)
            .reset_index()
        )
        player_data.rename(columns={"index": "Date"}, inplace=True)
        player_data["PlayerID"] = player_id

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
                        player_data[f"{col}-{dia}"] = (
                            player_data[col].rolling(window=dia, min_periods=1).sum()
                        )
                        player_data[f"{col}-{dia}-avg"] = (
                            player_data[col].rolling(window=dia, min_periods=1).mean()
                        )
                        player_data[f"{col}-{dia}-std"] = (
                            player_data[col].rolling(window=dia, min_periods=1).std()
                        )
                    else:
                        # Only rolling sum for other periods
                        player_data[f"{col}-{dia}"] = (
                            player_data[col].rolling(window=dia, min_periods=1).sum()
                        )

        # Drop rows where all calculated values are zero (rest days)
        mask_non_zero = player_data[columnas_calcular].sum(axis=1) > 0
        player_data = player_data[mask_non_zero]

        # Append the processed player's data to the list
        processed_players.append(player_data)

    # Concatenate all processed player DataFrames into a single DataFrame
    df_resultado = pd.concat(processed_players, ignore_index=True)

    return df_resultado


def filter_players(df):
    # Step 1: Select the rows with the latest date
    latest_date = df["Date"].max()
    latest_date_rows = df[df["Date"] == latest_date]

    # Step 2: Iterate through each row to check TD, TD-3, and TD7 values
    for index, row in latest_date_rows.iterrows():
        if row["TD"] == row["TD-3"] == row["TD-7"]:
            # Print PlayerID and drop the row
            print(f"PlayerID {row['PlayerID']} does not have enough information.")
            df = df.drop(index)
    

    df = df.reset_index(drop=True)

    return df


def calculate_fatigue_metrics(df, metrics):
    min_threshold = 1e-5  # Small constant to replace zeros

    # Calculate ACWR, MSWR for each metric
    for metric in metrics:
        # Replace zeroes with min value to avoid division by 0
        df[f"{metric}-21-avg"] = df[f"{metric}-21-avg"].replace(0, min_threshold)
        df[f"{metric}-7-std"] = df[f"{metric}-7-std"].replace(0, min_threshold)

        # Calculate 7-day and 28-day averages for ACWR
        df[f"{metric}_ACWR"] = df[f"{metric}-7-avg"] / df[f"{metric}-21-avg"]

        # Calculate mean and standard deviation for MSWR
        df[f"{metric}_MSWR"] = df[f"{metric}-7-avg"] / df[f"{metric}-7-std"]

    cumulative_df.drop(columns=columns_to_drop, inplace=True)

    return df


def session_OHE(df):
    # Strip spaces
    df["Session"] = df["Session"].str.replace(" ", "", regex=False)

    # Perform one-hot encoding
    encoded_df = pd.get_dummies(df, columns=["Session"], prefix="Session")

    one_hot_columns = [col for col in encoded_df.columns if col.startswith("Session_")]
    encoded_df[one_hot_columns] = encoded_df[one_hot_columns].astype(int)

    # encoded_df = final_df.dropna(subset=one_hot_columns)
    return encoded_df

import pandas as pd

def one_hot_encode_session(df, column_name, session_values):
    
    # Create column names for the one-hot encoding
    column_names = [f"Session_{'M' + s[2:] if '+' in s or '-' in s else s}" for s in session_values]
    
    # Initialize a zero-initialized DataFrame for one-hot encoding with the same index as the input DataFrame
    one_hot_df = pd.DataFrame(0, index=df.index, columns=column_names)

    # Correct mapping of session values to columns
    for idx in df.index:
        session = df.loc[idx, column_name]
        if session == 'MD':
            one_hot_df.loc[idx, 'Session_MD'] = 1
        else:
            one_hot_df.loc[idx, f"Session_M{session[2:]}"] = 1  # Handles both + and - cases
    
    # Concatenate the original DataFrame with the one-hot encoding DataFrame
    return pd.concat([df, one_hot_df], axis=1)

def process_data_testing(df):
    latest_date = df["Date"].max()
    latest_date_rows = df[df["Date"] == latest_date]

    columns_to_rename = ["TD", ">19.8", ">25", "ACC", "DEC", "Sprints", "Mins", "% Max Speed"]

    # Rename columns by adding -1
    latest_date_rows.rename(
        columns={col: f"{col}-1" for col in columns_to_rename}, inplace=True
    )

    target_sessions = ['MD', 'MD+1', 'MD+2', 'MD+3', 'MD-5', 'MD-4', 'MD-3', 'MD-2', 'MD-1']

    # Filter DataFrame
    latest_date_rows_filtered = latest_date_rows[latest_date_rows['Session'].isin(target_sessions)]
    
    latest_date_rows_filtered_OHE = one_hot_encode_session(latest_date_rows_filtered, 'Session', target_sessions)
    
    latest_date_rows_filtered_OHE = latest_date_rows_filtered_OHE.reset_index(drop=True)

    return latest_date_rows_filtered_OHE


# metrics_test = ['TD-1', '>19.8-1', '>25-1', 'ACC-1', 'DEC-1', 'Sprints-1','Mins-1', '% Max Speed-1', 'TD-3', '>19.8-3', '>25-3', 'ACC-3',
# 'DEC-3', 'Sprints-3', 'TD-7', '>19.8-7', '>25-7', 'ACC-7',
# 'DEC-7', 'Sprints-7', 'TD-21', '>19.8-21', '>25-21', 'ACC-21',
# 'DEC-21', 'Sprints-21', 'TD_ACWR', 'TD_MSWR', '>19.8_ACWR',
# '>19.8_MSWR', '>25_ACWR', '>25_MSWR', 'ACC_ACWR', 'ACC_MSWR',
# 'DEC_ACWR', 'DEC_MSWR']

metrics_test = ['TD-1', '>19.8-1', '>25-1', 'ACC-1', 'DEC-1', 'Sprints-1',
       'Mins-1', '% Max Speed-1', 'TD-3', '>19.8-3', '>25-3', 'ACC-3',
       'DEC-3', 'Sprints-3', 'TD-7', '>19.8-7', '>25-7', 'ACC-7',
       'DEC-7', 'Sprints-7', 'TD-21', '>19.8-21', '>25-21', 'ACC-21',
       'DEC-21', 'Sprints-21', 'TD_ACWR', 'TD_MSWR', '>19.8_ACWR',
       '>19.8_MSWR', '>25_ACWR', '>25_MSWR', 'ACC_ACWR', 'ACC_MSWR',
       'DEC_ACWR', 'DEC_MSWR','Session_M+1', 'Session_M+2', 'Session_M+3',
       'Session_M-1', 'Session_M-2', 'Session_M-3', 'Session_M-4',
       'Session_M-5', 'Session_MD']


if __name__ == "__main__":
    # Call the function to process files in the current directory
    data_df = read_files()

    if data_df is None:
        print("File reading failed. Exiting program.")
        exit()

    processed_df = data_processing(data_df)

    cumulative_df = calcular_acumulado(processed_df, cols_calculate_loads, [3, 7, 21])

    # Filter players with enough data
    filtered_df = filter_players(cumulative_df)

    complete_df = calculate_fatigue_metrics(filtered_df, cols_calculate_fatigues)

    data_df.MD.unique()

    test_df = process_data_testing(complete_df)

    test_df
    
    test_df_original = test_df.copy()

    #ANN

    # ann_model = joblib.load("xgb_classifier_model_ns.pkl") 
    # scaler = StandardScaler()

    # # Scale only the selected columns
    # X_test_scaled = scaler.fit_transform(test_df[metrics_test])

    # predictions = ann_model.predict(X_test_scaled) * 100
    # print(predictions)

    # XGB 

    # Load the classifier
    model = joblib.load("xgb_classifier_model_s1.pkl")
    
    predictions = model.predict_proba(test_df[metrics_test])[:, 1] * 100
    print(predictions)

    # Select PlayerID and Injury columns from the test_df_original
    aresult_df = test_df_original[['PlayerID', 'Injury']].copy()

    # Add the Probability column using the predictions
    aresult_df['Probability'] = predictions

    



    
