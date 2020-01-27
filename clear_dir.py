import re
import os
import shutil
from pathlib import Path

entry_prog = re.compile(r"^(\d{8})-.+$")
file_prog = re.compile(r"^(?:石井坡街道-\d{8}-.+?\.zip|.+?\.py|.+?\.txt)$")
cwd = os.getcwd()
with os.scandir(cwd) as entries:
    for entry in entries:
        m = entry_prog.match(entry.name)
        if (m is not None) and entry.is_dir():
            ymd = m.group(1)
            for filename in os.listdir(entry.path):
                m = file_prog.match(filename)
                if m is not None:
                    file_path = Path(entry.path) / filename
                    # print(file_path)
                    os.remove(file_path)
            ym = ymd[:-2]
            y = ym[:-2]
            dst_path = Path(cwd) / f"{y}/{ym}"
            if not dst_path.is_dir():
                os.makedirs(dst_path)
            # print(f"move {entry.name} to {dst_path}")
            shutil.move(entry.name, dst_path)