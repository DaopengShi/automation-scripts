import os
import shutil
import re

prog = re.compile(r"^(?:.+?)\.(?:jpg|png|jpeg|)$")
cwd = os.getcwd()

total_num = 0
with os.scandir(cwd) as entries:
    for entry in entries:
        if (not entry.name.startswith(".")) and entry.is_dir():
            entry_num = 0
            for name in os.listdir(entry.path):
                m = prog.match(name)
                if m is not None:
                    entry_num += 1
            total_num += entry_num
            print(f"{entry.name} has {entry_num} files")
            # print(f"copy files in {str(entry.path)} to {cwd}")
            shutil.copytree(entry.path, os.getcwd(), dirs_exist_ok=True)

import zipfile
from pathlib import Path

cwd_path = Path(cwd)
zip_name = f"石井坡街道-{cwd_path.name}-{total_num}条.zip"

# print(f"{zip_name}")
new_zip = zipfile.ZipFile(zip_name, "w")
with os.scandir(cwd) as entries:
    for entry in entries:
        if (not entry.name.startswith(".")) and entry.is_file():
            m = prog.match(entry.name)
            if m is not None:
                # print(f"add {entry.name} to zip file")
                new_zip.write(entry.name)
                os.remove(entry.path)
new_zip.close()

aws = input("Please press any key to continue!")