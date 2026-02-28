import pandas as pd
from config import OUTPUT_CSV

def save_processed_data(df: pd.DataFrame):
    df.to_csv(OUTPUT_CSV, index=False)