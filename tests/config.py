from pandas import read_csv

VERBOSE = True

ALERT = f"[!]"
INFO = f"[i]"

CORRELATION = 'corr'  #'sem'
CORRELATION_THRESHOLD = 0.99  # Less than 0.99 is undesirable

# Load sample_data from package resources
from importlib.resources import files as ir_files # For Python 3.9+
from pandas import DataFrame # Ensure DataFrame is imported for fallback

try:
    # Recommended way to access package data files
    data_file_path = ir_files('pandas_ta').joinpath('data', 'sample.csv')
    # Update read_csv call: remove infer_datetime_format and keep_date_col
    sample_data = read_csv(data_file_path, index_col=0, parse_dates=True)
except Exception as e:
    print(f"ERROR in tests/config.py: Could not load data/sample.csv using importlib.resources: {e}")
    print(f"Attempted path: {str(data_file_path) if 'data_file_path' in locals() else 'N/A'}")
    print(f"Make sure 'pandas_ta' is installed and the data file 'sample.csv' is in 'pandas_ta/data/'.")
    sample_data = DataFrame() # Empty DataFrame to allow tests to be collected

def error_analysis(df, kind, msg, icon=INFO, newline=True):
    if VERBOSE:
        s = f" {icon} {df.name}['{kind}']: {msg}"
        if newline: s = '\n' + s
        print(s)