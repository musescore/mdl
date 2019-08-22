import json
import zipfile
import os
import hashlib
import shutil

def recursive_zip(zipf, directory, folder=""):
    zipf.write(directory, folder)
    for item in os.listdir(directory):
        absolutePath = os.path.join(directory, item)
        if os.path.isfile(absolutePath) and item != ".DS_Store":
            zipf.write(absolutePath, folder + os.sep + item)
        elif os.path.isdir(absolutePath):
            recursive_zip(zipf, absolutePath, folder + os.sep + item)


outdir = "out"
shutil.rmtree(outdir, ignore_errors=True)
os.makedirs(outdir)

## read metadata.json
md_file = open("../resources/metadata.json", "r+")
md = json.load(md_file)
md_file.close()
extensionId = md['id']

# zip the extension
zipName = extensionId + '.muxt'
zipPath = os.path.join(outdir, zipName)
myzip = zipfile.ZipFile(zipPath, mode='w')
recursive_zip(myzip, os.path.abspath('../resources/instruments'), "instruments")
recursive_zip(myzip, os.path.abspath('../resources/sound'), "sfzs")
recursive_zip(myzip, os.path.abspath('../resources/templates'), "templates")
recursive_zip(myzip, os.path.abspath('../resources/workspaces'), "workspaces")
myzip.write('../resources/metadata.json', 'metadata.json')
myzip.close()
print("Packaging successful")

# compute zip size
fileSize = os.path.getsize(zipPath)
print(fileSize)

# compute SHA1 hash
f = open(zipPath, newline='\n', encoding='utf-8')
fileread = f.read()
hashfunc = hashlib.sha1(fileread)
f.close()
h = str(hashfunc.hexdigest())
print(h)

### create details.json
data = {}
data["type"] = "Extensions"
data["version"] = "2.0"

## read from metadata.json
data[extensionId] = {}
data[extensionId]["file_name"] = zipName
data[extensionId]["name"] = md["name"]
data[extensionId]["description"] = md["description"]
data[extensionId]["tags"] = md["tags"]
data[extensionId]["version"] = md["version"]

data[extensionId]["file_size"] = fileSize
data[extensionId]["hash"] = h

json_file = open(os.path.join(outdir, 'details.json'), "w")
json_file.write(json.dumps(data, sort_keys=True, indent=4))
json_file.close()
