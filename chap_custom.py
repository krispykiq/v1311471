import re

chap_custom = ""
chap_custom = chap_custom.replace(":", " ")
chap_custom = chap_custom.replace("notice.", "notice")
if chap_custom != "":
  chap_blacklist = r" new|	\w{3}.\d+\,.\d{4}| Ren| Lynn| Vvvvvv| osamu| \w{3}.\d+\,.\d{4}"
  # compiled_titles_blacklist = re.compile(f"({chap_blacklist})")


  chap_custom = re.sub(chap_blacklist, '', chap_custom)
  
  # cbzs = chap_custom.split(" ")
  chap_split = r"(?<=\d)\s(?=Ch\.\d*)|(?<=[a-z])\s(?=Ch\.\d*)|(?<=\d)\s(?=season)|(?<=\d{2})\s(?=[a-z])"
  cbzs = re.split(f"{chap_split}", chap_custom)
  

  # print(cbzs)
  for i in cbzs:
    print(i)