#@markdown ####Multiple Folders 
from subprocess import getoutput
from IPython.display import HTML
from google.colab import drive
import os
import time
import re
if os.path.isfile("/content/output.txt") == True:
  os.remove("/content/output.txt")

directory = "" #@param {type:"string"}
title = "" #@param {type:"string"}
description = "Note that if you're having troubles loading images, try (1) signing into a Google account on the browser you're using, and (2) enable cross-site cookies.\\n\\nRead retconned (no longer canon) chapters here: https://cubari.moe/read/gist/JRalY/\\n\\nContent hosted externally at https://drive.google.com/drive/folders/{id}" #@param {type:"string"}
cover = "" #@param {type:"string"}
author = "" #@param {type:"string"}
artist = "" #@param {type:"string"}

if os.path.isfile("/usr/bin/xattr") == False:
  !apt-get install xattr > /dev/null

fids = []
chaptnum = 1
fidscount = 1
chaptscount = 1

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

def chapts(directory2):
  global fids
  global chaptnum
  global directory
  global fidscount
  global chaptscount
  title = (directory2.split("/"))[-1]
  utx = time.time()

  listdir2 = os.listdir(directory2)
  sort_nicely(listdir2)
  for i in listdir2:
    
    fids.append(getoutput(f"xattr -p 'user.drive.id' '{directory2}/{i}' "))
  with open("/content/output.txt", "a") as f:
    f.write('''
      "%s": {
            "groups": {
                        "GDrive": [
''' % chaptnum)
  chaptnum+=1

  fidscount = 1
  with open("/content/output.txt", "a") as f:
    # print(len(fids))
    for i in fids:
      if fidscount == len(fids):
        f.write('                       "https://drive.google.com/uc?id=' + i + '"\n')
      else:
        f.write('                       "https://drive.google.com/uc?id=' + i + '",\n')
      # print(fidscount)
      fidscount+=1
    
    f.write("""                ]
            },
            """)
    
    # print(len(os.listdir(directory)))
    # print(chaptscount)
    if chaptscount == len(os.listdir(directory)):
          f.write("""  "last_updated": %s,
            "title": "%s",
            "volume": "1"
        }
        """ % (utx,title))
    else:
      f.write(""""last_updated": %s,
              "title": "%s",
              "volume": "1"
          },
          """ % (utx,title))
    chaptscount+=1
  
  fids= []






with open("/content/output.txt", "a") as f:
  f.write("""{
    "chapters": {""")

listidr = os.listdir(directory)
sort_nicely(listidr)

for i in listidr:
  directory2 = "%s/%s" % (directory, i)
  chapts(directory2)


with open("/content/output.txt", "a") as f:
  f.write("""
  },
    "cover": "%s",
    "description": "%s",
    "title": "%s",
    "author": "%s",
    "artist": "%s"
}""" % (cover, description, title, author, artist))

