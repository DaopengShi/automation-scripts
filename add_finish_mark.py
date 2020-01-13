import os
import re
from pathlib import Path

prog = re.compile(r"^(\d{4}\d{2}\d{2}-.+?)(f?)(\.(?:doc|docx))$")

for dirpath, dirnames, filenames in os.walk(".", topdown = False):
    for filename in filenames:
        if not filename.startswith("."):
            m = prog.match(filename)
            if (m is not None) and (m.group(2) == ""):
                src_file = Path(dirpath, filename)
                dst_filename = f"{m.group(1)}f{m.group(3)}"
                dst_file = Path(dirpath, dst_filename)
                os.replace(src_file, dst_file)

print("Done!")