import os
import pandas as pd
import bw2data as bd
from datetime import datetime

# you can run all databases at once, if you have them in a similar format to the example here
versions = ["391"] # ["391"] 
models = ['con', "cutoff", 'apos']
dbases = ["{}{}".format(x, y) for x in models for y in versions]
projects = ["WasteFootprint_{}".format(x) for x in dbases]

data_dir = os.getcwd()+"/data/"
price_dir = data_dir + "prices/"

start = datetime.now()

for dbase in dbases:
    
    start1 = datetime.now()
# set the bw2 project and database
    project = "WasteFootprint_{}".format(dbase)
    if project not in bd.projects:
        print("Project {} not found".format(project))
        continue 
    else:
        bd.projects.set_current(project)
    
    db = bd.Database(dbase)
    print("Adding price information to database: {} in project {}".format(dbase, project))
    
# load the price data files produced by ExtractPriceData.py
    price_file = price_dir + "{}_price_df.csv".format(dbase)
    df_prices = pd.read_csv(price_file, sep=";")

# load the activities from the database
    print("Loading activities from database...")
    acts_all = pd.DataFrame([x.as_dict() for x  in db])
    acts_all = acts_all[['code','name','location','flow']]

# combine the two dataframes so as to get the codes for the activities by matching the 'flow', 'name' and 'location' columns
    df = df_prices.merge(acts_all, on=['flow','name','location'], how='inner')
    df = df.reset_index(drop=True)
    
# edit each activity in the database to add the price data
    print("Adding prices to activities...")
    for i, row in df.iterrows():
        print(dbase, i+1,"/", df.shape[0], row["name"])
        act = db.get(row.code)
        act['price'] = row.amount
        act['currency'] = row.unit
        act.save()
    
    finish1 = datetime.now()
    duration = finish1 - start1
    
# print the number of activities with prices added
    acts_with_prices = pd.DataFrame([x.as_dict() for x  in db])[['name', 'price']]
    prices_added = acts_with_prices[acts_with_prices.price.notnull()].shape[0]
    print("Added {} prices to {}, which has {} activities, in {}".format(prices_added, dbase, acts_all.shape[0], str(duration).split(".")[0]))
    
# write a log entry
    with open(data_dir+"AddPricesToDB_log.txt", "a") as f:
        f.write("{} : Added {} prices to {} in project {}, which has {} activities, in {}\n".format(finish1.strftime("%Y-%m-%d %H:%M:%S"), prices_added, dbase, project, acts_all.shape[0], str(duration).split(".")[0]))
    

finish = datetime.now()
duration = finish - start
print("Processed {} databases in {}".format(len(dbases), str(duration).split(".")[0]))
    
    