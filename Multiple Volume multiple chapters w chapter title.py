#@markdown #### <font color=red>Multiple Volume multiple chapters w/ chapter title</font>
#@markdown #### <font size=1>Tested with:</font>
#@markdown #### <font size=1>The Strange Adventure of a Broke Mercenary v01-02 (2021) (Digital) (danke-Empire)</font>
import os
import re
from subprocess import getoutput
from IPython.display import HTML
from google.colab import drive
import time

directory = ""  #@param {type:"string"}
title = "" #@param {type:"string"}
description = "" #@param {type:"string"}
cover = "" #@param {type:"string"}
author = "" #@param {type:"string"}
artist = "" #@param {type:"string"}


# ======================CHANGABLE============================
blacklist = "" #@param {type:"string"}
reblacklist = re.compile(f"({blacklist})")
# ======================CHANGABLE============================

if os.path.isfile("/usr/bin/xattr") == False:
  !apt-get install xattr > /dev/null
fids = []
chaptnum = 1
fidscount = 1
chaptscount = 1
volcount = 1


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

if description == "":
  description = description + r"Note that if you're having troubles loading images, try (1) signing into a Google account on the browser you're using, and (2) enable cross-site cookies.\n\nContent hosted externally at https://drive.google.com/drive/folders/{id}"
else:
  description = description + r"\n———————————————————————————————————————————————————\nNote that if you're having troubles loading images, try (1) signing into a Google account on the browser you're using, and (2) enable cross-site cookies.\n\nContent hosted externally at https://drive.google.com/drive/folders/{id}"


cbzs = os.listdir(directory) # folder of volume
chdir = []  # ['c002']
nodups = [] 
ch_temp = []
filetitles = []
removecommacount = 1
lastvolcount = 1
ch_unedited = []
ch = [] # 1,2,3,4,5
sort_nicely(cbzs)
# ======================
nodups_titles = []
fix_titles = []

with open("/content/output.txt", "a") as f:
  f.write("""{
  "chapters": {""")

for cbz in cbzs:
  print(f"""
=========================================================
     {cbz}
=========================================================
  """)

  cbzfile = os.listdir(f"{directory}/{cbz}")

  sort_nicely(cbzfile)
  for img in cbzfile:
 
    if re.findall("(c\d)", img) != []:
      chdir.append(re.findall(r"(\bc\d*)", img))
      img = re.sub(reblacklist, '',img)
      filetitles.append(re.findall(r"(?<=\[).*(?=\])", img))

#=======GET CHAPTER NAME===========================
  if blacklist != "":
    for i in filetitles:
      if i not in nodups_titles:
        nodups_titles.append(i)

    for i in nodups_titles:
      fix_titles.append(str(i)[2:-2])
  
  else:
    pass
# =====================================================
# ============GET CHAPTER Number=================================
  for i in chdir:
    if i not in nodups:
      nodups.append(i)

  for i in nodups: # ['c001']
    ch_unedited.append(str(i)[2:-2]) # c001
    ch_temp.append((str(i))[3:-2]) # 001


  for i in ch_temp:
    ch.append(i.lstrip("0"))
# ==================================================
  sort_nicely(ch)
  for chap, unchap in zip(ch, ch_unedited):
    utx = time.time()
    print(f"""
-------------------------------------------------------------
                      {chap}
-------------------------------------------------------------
    """)

    if blacklist != "":
      print(f"{chap}: {fix_titles[int(chap) - 1]}")
      chaptitle = fix_titles[int(chap) - 1]
    else:
      chaptitle = f"Chapter {chap}"

    sort_nicely(cbzfile)
    sort_nicely(ch_unedited)
    for img in cbzfile:
      if unchap in img:
        fids.append(getoutput(f"xattr -p 'user.drive.id' '{directory}/{cbz}/{img}' "))

    with open("/content/output.txt", "a") as f:
      f.write('''
        "%s": {
            "groups": {
                  "GDrive": [
''' % chap)

    for fid in fids:
      if removecommacount == len(fids):
        with open("/content/output.txt", "a") as f:
          f.write(f'                         "https://drive.google.com/uc?id={fid}"\n')
      else:
        with open("/content/output.txt", "a") as f:
          f.write(f'                         "https://drive.google.com/uc?id={fid}",\n')

      removecommacount+=1

    with open("/content/output.txt", "a") as f:
      f.write("""                ]
            },
            """)
      
      print(f"volcount:{volcount}/{len(cbzs)}")
      print(f"chaptscount:{chaptscount}/{len(ch)}")

      if volcount == len(cbzs) and chaptscount == len(ch):
          f.write("""  "last_updated": %s,
            "title": "%s",
            "volume": "%s"
        }
        """ % (utx, chaptitle, volcount))
      else:
        f.write("""  "last_updated": %s,
                "title": "%s",
                "volume": "%s"
            },
            """ % (utx, chaptitle, volcount))
    removecommacount = 1
    chaptscount+=1
    print(f"total_count: {len(fids)}")
    # print(f"fids: {fids}")
    
    fids = []
      
  
  volcount +=1
  fix_titles = []
  chaptscount = 1
  ch_unedited = []
  ch = []
  ch_temp = []
  nodups = []
  chdir = []

with open("/content/output.txt", "a") as f:
  f.write("""
  },
    "cover": "%s",
    "description": "%s",
    "title": "%s",
    "author": "%s",
    "artist": "%s"
}""" % (cover, description, title, author, artist))



# https://stackoverflow.com/questions/44717271/how-to-ignore-the-specific-word-in-a-string-using-python-regular-expression