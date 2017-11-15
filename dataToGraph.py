import math

def lineToPoint(line):
    '''
    Takes a line that looks like this
    156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)
    and returns latitude and longitude value
    '''
    driverID, timeStamp, point = line.split(';')
    #POINT(41.8836718276551 12.4877775603346)
    latitude, longitude = point.replace('POINT(','').replace(')','').split(' ')
    latitude = float(latitude)
    longitude = float(longitude)
    return [latitude,longitude]

def MaxMinCoordinates(filename):
    '''Reads file and returns maximum and minimum values for longitudes and latitudes,
       A line looks like this:
       156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)
    '''
    max_latitude = -1
    min_latitude = -1
    max_longitude = -1
    min_longitude = -1

    with open(filename, "r") as fin:
        for line in fin:
            latitude, longitude = lineToPoint(line)

            if(max_latitude == -1 or latitude > max_latitude):
                max_latitude = latitude    
            if(max_longitude == -1 or longitude > max_longitude):
                max_longitude = longitude    
            if(min_latitude == -1 or latitude < min_latitude):
                min_latitude = latitude    
            if(min_longitude == -1 or longitude < min_longitude):
                min_longitude = longitude

    return [max_latitude,min_latitude,max_longitude,min_longitude]

def GetSuitableCoordinates(filename, latitude_width, longitude_width):
    '''
    Reads the file and finds suitable Max and Min coordinates    
    '''
    max_latitude, min_latitude, max_longitude, min_longitude = MaxMinCoordinates(filename)
    print(max_latitude) #51.4548789
    print(min_latitude) #39.3623147
    print(max_longitude) #16.2340827
    print(min_longitude) #-0.1453681

    totalLatitudeBuckets = int(math.floor((max_latitude - min_latitude) / latitude_width) + 1)
    totalLongitudeBuckets = int(math.floor((max_longitude - min_longitude) / longitude_width) + 1)
      
    latitudeBucketFrequency = [0] * totalLatitudeBuckets
    longitudeBucketFrequency = [0] * totalLongitudeBuckets

    with open(filename, "r") as fin:
        for line in fin:
            latitude, longitude = lineToPoint(line)
            latitudeBucketIndex = int(math.floor((latitude - min_latitude) / latitude_width))
            latitudeBucketFrequency[latitudeBucketIndex] += 1
            longitudeBucketIndex = int(math.floor((longitude - min_longitude) / longitude_width))
            longitudeBucketFrequency[longitudeBucketIndex] += 1

    #We have frequencies, Find buckets with highest frequency
    min_suitable_latitude = min_latitude + latitude_width * latitudeBucketFrequency.index(max(latitudeBucketFrequency))
    max_suitable_latitude = min_suitable_latitude + latitude_width

    min_suitable_longitude = min_longitude + longitude_width * longitudeBucketFrequency.index(max(longitudeBucketFrequency))
    max_suitable_longitude = min_suitable_longitude + longitude_width

    return [max_suitable_latitude,min_suitable_latitude,max_suitable_longitude,min_suitable_longitude]

def main():
    filename = "/home/aniket/Desktop/BTP/Travel Time Prediction/taxi_february.txt"
    latitude_width = 0.15 #Width of latitude required ~ 0.1 to 0.2
    longitude_width = 0.15 #Width of longitude required ~ 0.1 to 0.2
    max_suitable_latitude,min_suitable_latitude,max_suitable_longitude,min_suitable_longitude = GetSuitableCoordinates(filename,latitude_width,longitude_width)
    print("Suitable Coordinates : ")
    print(max_suitable_latitude)
    print(min_suitable_latitude)
    print(max_suitable_longitude)
    print(min_suitable_longitude)


if __name__=="__main__":
    main()

