import json
import os
import shutil

# If you want the data to be saved (default is always on, but you could change that here)
save = True

__json_file__ = "parameters/parameters.json"

if not os.path.exists("parameters/parameters.json"):
    shutil.copy("templates/parameters.json", "analysis/parameters.json")

with open("analysis/parameters.json", "r") as f:

    __parameters__ = json.load(f)

    # Could use something as:
    # # for k, v in __parameters__.items():
    # #     vars()[k] = v
    # ... but it is more convenient to give explicitly all the params (allows using of auto-complete)

    file_name = __parameters__["file_name"]
    span = __parameters__["span"]
    fit = __parameters__["fit"]
