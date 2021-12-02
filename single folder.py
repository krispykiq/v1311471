#@markdown ####Single Folder
from subprocess import getoutput
from IPython.display import HTML
from google.colab import drive
import os
import time
os.remove("/content/output.txt")
if os.path.isfile("/usr/bin/xattr") == False:
  !apt-get install xattr > /dev/null

fids = []
count = 1

directory = "" #@param {type:"string"}
description = "" #@param {type:"string"}
title = "" #@param {type:"string"}
cover = "" #@param {type:"string"}
volume = "" #@param {type:"string"}
chaptitle = "" #@param {type:"string"}


for i in os.listdir(directory):
  fids.append(getoutput(f"xattr -p 'user.drive.id' '{directory}/{i}' "))


with open("output.txt", "w") as f:
  f.write("""{
    "chapters": {
        "1": {
            "groups": {
                "GDrive": [""")
  print(len(fids))
  for i in fids:

    print(count)
    if count == len(fids):
      f.write('"https://drive.google.com/uc?id=' + i + '"\n')
    else:
      f.write('"https://drive.google.com/uc?id=' + i + '",\n')
    
    count += 1
  time = time.time()
  f.write("""                ]
          },""")
  f.write("""  "last_updated": %s,
          "title": "%s",
          "volume": "%s"
      }""" % (time, chaptitle, volume))
  f.write("""    "cover": "%s",
  "description": "%s",
  "title": "%s"
}""" % (cover, description, title))
