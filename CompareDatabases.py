import pandas as pd
import os

# load the price data files produced by ExtractPriceData.py
price_dir = os.getcwd() +"/data/prices/"
files = [x for x in os.listdir(price_dir) if "price_df.csv" in x]

# count the number of price data for each database
prices = []
for f in files:
    file = os.path.join(price_dir, f) 
    price = {}
    df = pd.read_csv(file, sep=";")
    db = f.replace("_price_df.csv", "")
    print(df.shape[0],"\t",db)
    price.update({"db": db, "count":df.shape[0]})
    prices.append(price)
    
# save the results... 
# (anything before ei39 is really quite bad < 25% complete)
df = pd.DataFrame(prices)
df.to_csv("data/number_of_price_data_by_database.csv", sep=",", index=False)