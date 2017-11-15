import json

jsonfilename = '/home/aniket/Desktop/BTP/Travel Time Prediction/cache/48d5fdd4ee518f36cfa23b4410c06176.json'

file = open(jsonfilename, 'r')
parsed = json.load(file)
file.close()

file = open(jsonfilename, 'w')
file.write(json.dumps(parsed, indent=2))