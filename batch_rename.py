import os
import re


def meta_data(dirpath, prog_dir, prog_file, filenames):
    names = []
    count = 0

    _, base_name = os.path.split(dirpath)
    m = prog_dir.match(base_name)
    if m is not None:
        exts = []
        for filename in filenames:
            if not filename.startswith("."):
                m = prog_file.match(filename)
                if m is not None:
                    names.append(filename)
                    ext = m.group(1)
                    exts.append(ext)
                    count += 1

        dst_nums = set(map(lambda x: str(x), range(1, count+1)))
        src_files = []
        src_exts = []
        pattern = r"{}".format(f"^{base_name}(\d*).(?:jpg|png|jpeg)$")
        prog = re.compile(pattern, flags = re.I)
        for name, ext in zip(names, exts):
            m = prog.match(name)
            if m is not None:
                src_num = m.group(1)
                if src_num in dst_nums:
                    dst_nums.remove(src_num)
                else:
                    src_file = os.path.join(dirpath, name)
                    src_files.append(src_file)
                    src_exts.append(ext)
            else:
                src_file = os.path.join(dirpath, name)
                src_files.append(src_file)
                src_exts.append(ext)

        dst_files = []
        for src_file, src_ext, dst_num in zip(src_files, src_exts, dst_nums):
            dst_file = os.path.join(dirpath, f"{base_name}{dst_num}.{src_ext.lower()}")
            dst_files.append(dst_file)
        return zip(src_files, dst_files)
    else:
        return None


def rename_batch(src_files_dist_files):
    for src_file, dst_file in src_files_dist_files:
        os.replace(src_file, dst_file)


prog_dir = re.compile(r"^\d{4}\d{2}\d{2}-.+$")
prog_file = re.compile(r"^.+\.(jpg|png|jpeg)$", flags=re.I)

for dirpath, dirnames, filenames in os.walk(".", topdown = False):
    src_files_dst_files = meta_data(dirpath, prog_dir, prog_file, filenames)
    if src_files_dst_files is not None:
        rename_batch(src_files_dst_files)