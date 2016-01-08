from os import listdir
from os.path import isfile, join
import json
files = list(listdir('/directory/to/list'))
files = filter(lambda k: '.zip' in k, files)
print files
f = open("/output/directory/last.json", 'w')
json.dump(files,f)
f.close()