# Link-Travel-Time-prediction

Dataset Source:
The dataset has been taken from CRAWDAD, a community resource for archiving
wireless data at Dartmouth. It is a dataset of mobility traces of taxi cabs in Rome,
Italy for the month of February in year 2014, for around 300 drivers.

The data is a txt file of around 1.6 GB formatted as:
DriverID;Timestamp;Position
Where:- DriverID is an integer ranging from 1 to 300,
Timestamp includes date and time,
Position is formatted as POINT(latitude,longitude)

An example is shown below

156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)

187;2014-02-01 00:00:01.148457+01;POINT(41.9285433333333 12.4690366666667)

297;2014-02-01 00:00:01.220066+01;POINT(41.8910686119733 12.4927045625339)

89;2014-02-01 00:00:01.470854+01;POINT(41.7931766914244 12.4321219603157)



Preprocessing Steps:
Selecting Suitable Window:
• We first find out the maximum longitude and latitude and similarly minimum
longitude and latitude.

• We divide whole region into grid of 0.15 × 0.15 squares.

• We then find the square where maximum number of the data points lie.
Cleansing of Graph Using OSMnx:

• Used the OSMnx python library to download the map of Rome for the desired
region.

• cleaned it to remove reduntant nodes lying in between the edges.

• Finally it results in text file containing nodes and edges of the graph.

Filtering Taxi Data:

• In this step, we filter those data points that lie within our desired region.

• Since the data is samples every 7 seconds, We have a lot of redundant data points
which lie in the middle of a road.

• To remove the redundant data, for each taxi locations we found the closest node in
the graph using Locality Sensitive Hashing (Ref: lshash Python library).

• If the closest node lies within a threshold of the actual data point then we replace
the actual location with the map node , else the data point is removed.



Extracting Link Durations:

• To find which link a driver is travelling through , we divide the data into 300 files
based on driver ids where each file contains data for one driver.

• We then traverse each file one by one .

• For each file we see driver’s locations at consecutive time stamps and check if this
corresponds to an edge in the map.

• If it does we add the current link , duration, timestamp in the output file. Else we
ignore the data point.

• Now we select a particular edge and extracted data corresponding to this edge and
sort it by timestamp and write to a new file.

• This file contains the Timestamp and duration for a particular edge in CSV format
sorted by timestamp.
