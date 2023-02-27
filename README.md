# Price data for LCA

## ExtractPriceData.py
* searches the .spold files from an EcoInvent database and extracts price data and metadata
* makes a csv file of the data
#### For example:
|amount |unit   |comment                                                                         |flow                                |name                                                    |location|
|-------|-------|--------------------------------------------------------------------------------|------------------------------------|--------------------------------------------------------|--------|
|0.0083 |EUR2005|Same calculations in file R61. The variations is due to industry price per MJ....|1f6c6d72-b328-4f8b-841b-5e0ecb494989|transport, pipeline, onshore, long distance, natural gas|KW      |
|0.127  |EUR2005|Calculated relative to 'Irrigating' ids 6978. Ecoinvent report 15, top page 65: 1/1200|3f5f5aef-3833-43d4-8b81-44123105afd7|irrigation, surface                                     |BR      |
|176.641|EUR2005|Calculated based on inputs: The price of the product has been calculated as a...|90055e28-2463-4a3f-bf50-f6f408085b8e|garage construction, wood, non-insulated, fire-protected|CH      |

## AddPricesToDBs.py
* reads csv file from previous script and uses brightway2 to edit the database, adding the missing price data

## CompareDatabases.py
* scans a set of databases and returns a table with the number of activities that have price data
#### For example:
|EI Database|Price data count|
|-----------|----------------|
|apos391    |17845           |
|cutoff39   |17439           |
|cutoff391  |17425           |
|con391     |14634           |
|con39      |14634           |
|cutoff38   |4342            |
|apos38     |4309            |
|con38      |4211            |
|cutoff35   |3418            |
|apos35     |3413            |
|con35      |3229            |