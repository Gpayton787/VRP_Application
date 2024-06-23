import pandas as pd



#Functions:
#1. Reads the CSV file into a pandas DataFrame
#2. Processes the data to be used in the solver (See README for processing information)

def csv_reader(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Return the DataFrame
    return df

def csv_to_dict(df):
    #Get all the addresses
