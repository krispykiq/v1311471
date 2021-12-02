import os
import re
from subprocess import getoutput
import datetime
from google.colab import drive
import calendar
import time

directory = "" #@param {type:"string"} 
title = "" #@param {type:"string"} 
description = "" #@param {type:"string"} 
cover = "" #@param {type:"string"} 
author = "" #@param {type:"string"} 
artist = "" #@param {type:"string"} 

if cover == "":
  cover = "https://drive.google.com/uc?id="

# ================TIME===================================
times = "" #@param {type:"string"} 

if times.replace(" ","").isdecimal() == True or times.replace("|","").isdecimal() == True:
  times = times.split("|")
else:
  times = re.findall(r"\w{3}.\d+\,.\d{4}", times)
  times.reverse()

# ===================TIME=============================

# ================TITLE BLACKLIST=======================
blacklist = "" #@param {type:"string"} 
reblacklist = re.compile(f"({blacklist})")
# ================TITLE BLACKLIST=======================

# =========================CUSTOM_TITLES======================
chap_custom = "" #@param {type:"string"} 
chap_custom = chap_custom.replace(":", " ")
chap_custom = chap_custom.replace("notice.", "notice")
if chap_custom != "":
  chap_blacklist = "" #@param {type:"string"}
  # compiled_titles_blacklist = re.compile(f"({chap_blacklist})")

  chap_custom = re.sub(chap_blacklist, '', chap_custom)
  
  chap_split = "" #@param {type:"string"}
  if chap_split != "":
    cbzs = re.split(f"{chap_split}", chap_custom)
  else:
    cbzs = chap_custom.split(" ")

  
  cbzs.reverse()

# ====================================================

if os.path.isfile("/usr/bin/xattr") == False:
  !apt-get install xattr > /dev/null
fids = []
chaptnum = 1
fidscount = 1
chaptscount = 1
volcount = 0
voltog = False

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

title = title.replace('"', r'\u0022',)
title = title.replace("'", r"\u0027")
title = title.replace("<", r"\u003C")
title = title.replace(">", r"\u003E")
title = title.replace("&", r"\u0026")

description = description.replace('"', r'\u0022',)
description = description.replace("'", r"\u0027")
description = description.replace("<", r"\u003C")
description = description.replace(">", r"\u003E")
description = description.replace("&", r"\u0026")

if description == "":
  description = description + r"Note that if you're having troubles loading images, try (1) signing into a Google account on the browser you're using, and (2) enable cross-site cookies.\n\nContent hosted externally at https://drive.google.com/drive/folders/{id}"
else:
  description = description + r"\n———————————————————————————————————————————————————\nNote that if you're having troubles loading images, try (1) signing into a Google account on the browser you're using, and (2) enable cross-site cookies.\n\nContent hosted externally at https://drive.google.com/drive/folders/{id}"
if chap_custom == "":
  cbzs = os.listdir(directory) # folder of volume
  sort_nicely(cbzs)
chdir = []  # ['c002']
nodups = [] 
ch_temp = []
filetitles = []
removecommacount = 1
lastvolcount = 1
iteratetitle = 0
timeiterate = 0
ch_unedited = []
ch = [] # 1,2,3,4,5
months = {month: index for index, month in enumerate(calendar.month_abbr) if month}

# ======================
nodups_titles = []
fix_titles = []
vols = []
vol_nodups = []
with open("/content/output.txt", "a") as f:
  f.write("""{
  "chapters": {""")

for cbz in cbzs:
  if cbz.endswith(".jpg") or cbz.endswith(".jpeg") or cbz.endswith(".png"):
    pass
  else:  
    print(f"""
  =========================================================
      {cbz}
  =========================================================
    """)
  # print(cbz) # folder of volume


  cbzfile = os.listdir(f"{directory}/{cbz}")

  # for img in cbzfile:
  #   print(img)
  sort_nicely(cbzfile)
  
  # for img in cbzfile:
  #   print(img)
  #   pass
  if re.findall(r"Vol\.\d*", cbz) != []:
    voltog = True
    vols.append(re.findall(r"Vol\.\d*", cbz))
  else:
    voltog = False
    volcount = 1

  if voltog == True:
    for i in vols:
      if i not in vol_nodups:
        vol_nodups.append(i)
        volcount +=1
  

  if chap_custom == "":
    if re.findall("Ch\.\d", cbz) != []:
      chdir.append(re.findall(r"Ch\.\d*\.?\d*", cbz))

    elif re.findall("Chapter.\d", cbz) != []:
      chdir.append(re.findall(r"Chapter.\d*\.?\d*", cbz))
  else:
    chdir.append(cbz)

  filetitles.append(cbz)

#=======GET CHAPTER NAME===========================
  if blacklist != "":
    for i in filetitles:
      i = re.sub(reblacklist, '',i)
      # print(i)
      # if i not in nodups_titles:
      if i == []:
        i = f"Chapter {chap}"
      nodups_titles.append(i)

    for i in nodups_titles:
      # print(i)
      fix_titles.append(str(i))

  else:
    pass

# =====================================================
# ============GET CHAPTER Number=================================
  for i in chdir:
    # if i not in nodups:
    #   nodups.append(i)

  # for i in nodups: # ['c001']
    if chap_custom == "":
      ch_unedited.append(str(i)[2:-2]) # c001
      if re.findall("Ch\.\d", cbz) != []:
        ch_temp.append((str(i))[5:-2]) # 001
      elif re.findall("Chapter.\d", cbz) != []:
        ch_temp.append((str(i))[9:-2])
    else:
      ch.append(i)
      ch_unedited.append(i)


  for i in ch_temp:

    i = i.lstrip("0")
    if i == "":
      ch.append(str(0))
    else:
      ch.append(i)


# ==================================================
  sort_nicely(ch)
  for chap, unchap in zip(ch, ch_unedited):

    if times == ['']:
      utx = time.time()
    else:
      date = (times[timeiterate].replace(",", "")).split(" ")

      if date[0].isdecimal() == True:
        utx = date[0]
      else:
        date = datetime.datetime(month=months.get(date[0].capitalize()), day=int(date[1]), year=int(date[2]))
        utx = int(time.mktime(date.timetuple()))


#     print(f"""
# -------------------------------------------------------------
#                       {chap}
# -------------------------------------------------------------
#     """)

    if blacklist != "":
      if blacklist == "own_title":
        chaptitle = cbz
      else:
        # print(f"{chap}: {fix_titles[int(iteratetitle)]}")
        # chaptitle = fix_titles[int(iteratetitle)]
        # print(f"{chap}: {fix_titles[-1]}")
        chaptitle = fix_titles[-1]
    else:
      chaptitle = f"Chapter {chap}"

    sort_nicely(cbzfile)
    sort_nicely(ch_unedited)
    
    for img in cbzfile:
      fids.append(getoutput(f"xattr -p 'user.drive.id' \"{directory}/{cbz}/{img}\" "))
    
    if chap_custom != "":
      chap = chaptscount

    print(f"{chap}: {fix_titles[-1]}")

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
      
      # print(f"volcount:{volcount}/{len(cbzs)}")
      print(f"volcount:{volcount}")
      print(f"chaptscount:{chaptscount}/{len(cbzs)}")
      if chaptscount == len(cbzs):
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

    print(f"total_count: {len(fids)}")
    print(f"imgs: {cbzfile}")
    print(f"fids: {fids}")

    datetme = re.sub(r"\d{2}:\d{2}:\d{2}", "", (datetime.datetime.utcfromtimestamp(utx).strftime('%Y-%m-%d %H:%M:%S')))
    print(f"time: {datetme} | {utx}")
    
    fids = []
  
  timeiterate+=1
  chaptscount+=1
  iteratetitle += 1
  fix_titles = []
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


# https://stackoverflow.com/questions/3418050/month-name-to-month-number-and-vice-versa-in-python
# https://stackoverflow.com/questions/44717271/how-to-ignore-the-specific-word-in-a-string-using-python-regular-expression