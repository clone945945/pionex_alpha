# Import the pandas library with the alias 'pd'
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('/content/241k-Singapore-pionex.com-Crypto-Trading-Bots-UsersDB-csv-2023.csv')

# Function to check for missing values
def check_missing_values(df):
    missing_values = df.isnull().sum()
    missing_summary = missing_values[missing_values > 0].sort_values(ascending=False)

    if missing_summary.empty:
        print("No missing values found in the dataset.")
    else:
        print("Missing values found in the following columns:")
        print(missing_summary)

# Function to check for duplicate rows
def check_duplicates(df):
    duplicate_rows = df[df.duplicated()]

    if duplicate_rows.empty:
        print("No duplicate rows found.")
    else:
        print(f"Number of duplicate rows: {len(duplicate_rows)}")
        print(duplicate_rows.head())  # Display the first few duplicate rows

# Function to check for outliers using IQR method
def check_outliers(df):
    outliers_info = {}

    # Checking for numerical columns only
    numerical_columns = df.select_dtypes(include=['number']).columns

    for column in numerical_columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Find outliers
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

        if not outliers.empty:
            outliers_info[column] = len(outliers)

    if outliers_info:
        print("Outliers found in the following columns:")
        for col, count in outliers_info.items():
            print(f"{col}: {count} outliers")
    else:
        print("No outliers found.")

# Run checks
check_missing_values(df)
check_duplicates(df)
check_outliers(df)




import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = '/content/241k-Singapore-pionex.com-Crypto-Trading-Bots-UsersDB-csv-2023.csv'
df = pd.read_csv(file_path)

# List of columns to drop
columns_to_drop = ['Lang', 'BrandCode']

# Save the dropped columns to a new DataFrame
dropped_columns_df = df[columns_to_drop]

# Save the dropped columns to 'drop_columns.csv'
dropped_columns_file = '/content/drop_columns.csv'
dropped_columns_df.to_csv(dropped_columns_file, index=False)

# Drop the specified columns from the original DataFrame
df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# Overwrite the original CSV file with the updated DataFrame
df.to_csv(file_path, index=False)

print("Specified columns have been dropped from the main file and saved to 'drop_columns.csv'. The main file has been updated.")




import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = '/content/241k-Singapore-pionex.com-Crypto-Trading-Bots-UsersDB-csv-2023.csv'
df = pd.read_csv(file_path)

# Convert 'RegistrationDate' to the format 'dd.mm.yy' and rename to 'reg_data'
df['RegistrationDate'] = pd.to_datetime(df['RegistrationDate'], errors='coerce').dt.strftime('%d.%m.%y')
df.rename(columns={'RegistrationDate': 'reg_data'}, inplace=True)

# Capitalize 'First Name' and 'Last Name', and rename them to 'first_name' and 'last_name'
df['First Name'] = df['First Name'].str.capitalize()
df['Last Name'] = df['Last Name'].str.capitalize()
df.rename(columns={'First Name': 'first_name', 'Last Name': 'last_name'}, inplace=True)

# Ensure 'Phone' is treated as a string
df['Phone'] = df['Phone'].astype(str)

# Save the modified DataFrame back to the original file (or specify a new path)
df.to_csv(file_path, index=False)

print("Data transformations completed and main file has been updated.")





import pandas as pd
import re
import os

# Load the CSV file into a pandas DataFrame
file_path = '/content/241k-Singapore-pionex.com-Crypto-Trading-Bots-UsersDB-csv-2023.csv'
df = pd.read_csv(file_path)

# Reorder columns
desired_order = ['first_name', 'last_name', 'Phone', 'Country', 'Email', 'reg_data']
df = df.reindex(columns=desired_order)

# Check for missing values in any row
missing_values_df = df[df.isnull().any(axis=1)]

# Define a regular expression pattern to validate email addresses
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Function to validate email addresses
def is_valid_email(email):
    if isinstance(email, str) and email:  # Check if email is non-empty string
        return bool(re.fullmatch(email_pattern, email))
    return False

# Identify invalid emails
invalid_emails_df = df[~df['Email'].apply(is_valid_email)]

# Combine rows with NaN values or invalid emails
garbage_df = pd.concat([missing_values_df, invalid_emails_df]).drop_duplicates()

# Save rows with NaN values or invalid emails to garbagePionex.csv
garbage_file = '/content/garbagePionex.csv'
garbage_df.to_csv(garbage_file, index=False)

# Remove rows with NaN values or invalid emails from the main DataFrame
df_cleaned = df.drop(garbage_df.index)

# Save the cleaned DataFrame back to the main CSV file
df_cleaned.to_csv(file_path, index=False)

print("Columns reordered and main file updated. Rows with NaN values or invalid emails saved to garbagePionex.csv.")

