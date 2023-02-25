import os
import pandas as pd
import bw2data as bd
import bw2io as bi
from bw2io import SingleOutputEcospold2Importer
from py7zr import SevenZipFile

# set up the directories
data_dir = os.getcwd()+"/data/"
db_dir = os.getcwd()+"/data/dbs/"
price_dir = os.getcwd() +"/data/prices"
if not os.path.isdir(data_dir): os.mkdir(os.getcwd()+"/data")
if not os.path.isdir(db_dir): os.mkdir(db_dir)
if not os.path.isdir(price_dir): os.mkdir(price_dir)
 
# find the database zip files
db_files = [x for x in os.listdir(db_dir) if ".7z" in x]
project_prefix = 'WasteFootprint_'


for db_file in db_files:

# load the bw2 project
    db_name = db_file.replace(".7z", "")
    print("\nUsing project: "+project_prefix+db_name)
    bd.projects.set_current(project_prefix+db_name)

# this part is just unzipping the databases
    if not os.path.isdir(db_dir+db_name):
        print("\nExtracting database "+db_name+"...")
        with SevenZipFile(db_dir+db_file, 'r') as archive:
            archive.extractall(path=db_dir+db_name)

# load the annoying ecospold2 files
    datasets = db_dir+db_name+"/datasets/" # change this to the path to your datasets, or move them to "$CWD/data/dbs/"
    db = bi.SingleOutputEcospold2Importer(datasets, db_name)
    activities = db.data

# find those that have prices
    price_list = []
    for x in activities:
        try:
            price = x["exchanges"][0]["properties"]["price"]
            flow = x["exchanges"][0]["flow"]
            name = x["name"]
            loc = x["location"]
            price.update({"flow": flow, "name": name, "location": loc})
            price_list.append(price)
        except Exception as e:
            pass
    
# make a dataframe of the price data, drop the zeros and duplicates, then save it
    df = pd.DataFrame(price_list) #6156
    df = df[df.amount != 0]
    df = df.drop_duplicates().reset_index(drop=True)
    df.to_csv(price_dir+db_name+"_price_df.csv", sep=";", index=False)
    
    
