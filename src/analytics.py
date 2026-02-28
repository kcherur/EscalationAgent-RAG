import pandas as pd

def category_negative_counts(df: pd.DataFrame):
    print("----------------------------")
    print("prinf df from analytics.py")
    #print(df)
    return (
        df[df["sentiment"] == "Negative"]
        .groupby("category")
        .size()
        .reset_index(name="negative_count")
        .sort_values("negative_count", ascending=False)
    )