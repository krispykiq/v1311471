import json
import os
import shutil
for i in os.listdir(os.getcwd()):
    if i != "organize.py" and i != ".git" and i != ".vscode" and i != "organized.py" and os.path.isdir(i) == False:
        print(i)
        with open(i, "r") as f:
            json_contents = f.read()
 
        parse_json = json.loads(json_contents)

        json_title = parse_json["title"]
        print(json_title + "\n")

        if os.path.exists((json_title[0]).capitalize()) == False:
            os.mkdir((json_title[0]).capitalize())
            shutil.move(i, (json_title[0]).capitalize())
        else:
            shutil.move(i, (json_title[0]).capitalize())

print("Finished")
