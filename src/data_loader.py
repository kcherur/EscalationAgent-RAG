import pandas as pd

def load_data():
    orders_df = pd.read_csv("data/orders.csv")
    reviews_df = pd.read_csv("data/reviews.csv")

    user_orders = (
        orders_df.groupby("user_id")["product_name"]
        .apply(list)
        .to_dict()
    )

    return reviews_df, user_orders