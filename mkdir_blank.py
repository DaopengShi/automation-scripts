import os
import shutil
import re
from datetime import date
from pathlib import Path

curr_date = date.today()
curr_year = str(curr_date.year)
curr_month = str(curr_date.month).rjust(2, "0")
curr_day = str(curr_date.day).rjust(2, "0")

dir_name = f"{curr_year}{curr_month}{curr_day}-"
pattern = r"{}".format(f"^{dir_name}(\d{{0,2}})$")
prog = re.compile(pattern)

total_num = 0
cwd = os.getcwd()
with os.scandir(cwd) as entries:
    for entry in entries:
        if (not entry.name.startswith(".")) and entry.is_dir():
            m = prog.match(entry.name)
            if m is not None:
                total_num += 1


if total_num != 0:
    dir_name = f"{dir_name}{total_num+1}"

dir_path = Path(dir_name)
community_names = ["中心湾", "和平山", "光荣坡", "远祖桥", "建设坡", "团结坝"]

for community_name in community_names:
    subdir_path = dir_path / community_name
    # print(f"{subdir_path} is created!")
    os.makedirs(subdir_path)

shutil.copy("extract_to_cwd_and_zip.py", dir_path)

