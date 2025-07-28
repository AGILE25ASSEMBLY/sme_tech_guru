# 01_prepare_data.py
import pandas as pd
import pickle
import re
import os

print("--- Starting Data Preparation Script ---")

# --- Configuration ---
# IMPORTANT: Ensure the Google Sheet is set to "Anyone with the link" can view.
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/10t0HyrDlXEkzQZKbCnOB_IzHiNAiblOqIlgF4m_nwoI/edit?usp=sharing"
PICKLE_FILENAME = 'faculty_data.pkl'

# --- Main Data Preparation Logic ---
def fetch_and_prepare_data(sheet_url, output_filename):
    """
    Fetches data from Google Sheet, processes it, and saves to a pickle file.
    """
    try:
        spreadsheet_id = sheet_url.split('/d/')[1].split('/')[0]
        csv_export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"

        print(f"Attempting to read data from: {csv_export_url}")
        df = pd.read_csv(csv_export_url)
        print("Data read successfully from Google Sheet.")

        if 'Timestamp' in df.columns:
            df = df.drop(columns=['Timestamp'])
            print("Dropped 'Timestamp' column.")

        original_columns = df.columns.tolist()
        cleaned_to_standard_map = {}

        for col in original_columns:
            cleaned_col = re.sub(r'[^a-zA-Z0-9_ ]', '', col)
            cleaned_col = cleaned_col.replace(' ', '_').lower()

            if "enter_your_name_capital_letters_are_preferred" in cleaned_col:
                cleaned_to_standard_map[col] = 'faculty_name'
            elif "select_your_department" in cleaned_col:
                cleaned_to_standard_map[col] = 'department'
            elif "kindly_select_the_your_respective_specialization" in cleaned_col:
                cleaned_to_standard_map[col] = 'specialization'
            elif "experience_in_the_relevant_specialization" in cleaned_col:
                cleaned_to_standard_map[col] = 'experience'
            elif "number_of_research_paper_published_so_far" in cleaned_col:
                cleaned_to_standard_map[col] = 'research_papers'
            elif "kindly_give_me_the_links_of_the_google_scholar" in cleaned_col:
                cleaned_to_standard_map[col] = 'google_scholar_link'
            elif "are_you_currently_teaching_subject_related_to_your_specialization" in cleaned_col:
                cleaned_to_standard_map[col] = 'currently_teaching'
            else:
                cleaned_to_standard_map[col] = cleaned_col

        df = df.rename(columns=cleaned_to_standard_map)
        print("Renamed and standardized column names.")

        if 'currently_teaching' in df.columns:
            df['currently_teaching'] = df['currently_teaching'].apply(
                lambda x: 'Yes' if str(x).strip().lower() == 'yes' else 'No'
            )
            print("Standardized 'currently_teaching' column to 'Yes'/'No'.")
        else:
            print("Warning: 'currently_teaching' column not found after renaming.")

        required_cols = ['faculty_name', 'department', 'specialization', 'currently_teaching']
        for col in required_cols:
            if col not in df.columns:
                print(f"Error: Required column '{col}' is missing after data processing. Please check your Google Sheet header names.")
                return

        df.to_pickle(output_filename)
        print(f"\nData successfully processed and saved to {output_filename}")
        print("\nFirst 5 rows of the processed data (final column names):")
        print(df.head().to_string())
        print(f"\nTotal rows processed: {len(df)}")

    except pd.errors.EmptyDataError:
        print("Error: The CSV data from the Google Sheet is empty or could not be parsed.")
        print("Please check if the sheet contains data and is shared correctly.")
    except Exception as e:
        print(f"\nAn error occurred during data fetching or processing: {e}")
        print("Possible reasons:")
        print("1. Internet connection issue.")
        print("2. Google Sheet URL is incorrect or sheet is not publicly accessible (check sharing settings).")
        print("3. Original column names in your sheet might have changed unexpectedly.")

if __name__ == "__main__":
    fetch_and_prepare_data(GOOGLE_SHEET_URL, PICKLE_FILENAME)
    print("\n--- Data Preparation Script Finished ---")
