import os

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

        # Get the latest date in the DATE column
        latest_date = df_gps["DATE"].max()
        # Example merge operation
        merged_df = pd.merge(df_gps, df_speed, on="DATE", how="inner")

        print("DataFrames processed and merged successfully.")
        return merged_df

    except KeyError as key_error:
        print(
            f"KeyError: {key_error}. Check if the 'DATE' column exists in both DataFrames."
        )
        return None

    except Exception as e:
        print(f"An error occurred while processing and merging DataFrames: {e}")
        return None


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

    if merged_df is not None:
        print("\nMerged DataFrame Preview:")
        print(merged_df.info())
