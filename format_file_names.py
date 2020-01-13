import os
import re


def meta_data(prog, filenames):
	infos = {}
	for filename in filenames:
		if not filename.startswith("."):
			m = prog.match(filename)
			if m is not None:
				year = m.group(1)
				month = m.group(2)
				day = m.group(3)
				event = m.group(4)
				num = m.group(5)
				ext = m.group(6)

				src_base = f"{year}{month}{day}-{event}"

				dst_month = month[1:] if month.startswith("0") else month
				dst_day = day[1:] if day.startswith("0") else day

				dst_base = f"{year}年{dst_month}月{dst_day}日，{event}"

				if src_base not in infos:
					infos[src_base] = {}
					infos[src_base]["src_base"] = src_base
					infos[src_base]["dst_base"] = dst_base
					infos[src_base]["count"] = 1
					infos[src_base]["src_nums"] = [num]
					infos[src_base]["src_exts"] = [ext]
				else:
					infos[src_base]["count"] = infos[src_base].get("count") + 1
					infos[src_base]["src_nums"].append(num)
					infos[src_base]["src_exts"].append(ext)

	return infos


def format_name(dirpath, infos):
	for src_base, info in infos.items():
		src_num_ext_dst_num = zip(info["src_nums"], info["src_exts"], range(1, info["count"]+1))
		for src_num, src_ext, dst_num in src_num_ext_dst_num:
			src_name = f"{info['src_base']}{src_num}.{src_ext}"
			src_file = os.path.join(dirpath, src_name)

			dst_name = f"{info['dst_base']}.{src_ext.lower()}" \
						if info["count"] == 1 else f"{info['dst_base']}{dst_num}.{src_ext.lower()}"
			dst_file = os.path.join(dirpath, dst_name)

			os.replace(src_file, dst_file)
			# print(f"format {src_file} to {dst_file}")


prog = re.compile(r"^(\d{4})(\d{2})(\d{2})-(.+?)(\d*)\.(jpg|png|jpeg)$", flags = re.I)


for dirpath, dirnames, filenames in os.walk(".", topdown = False):
	infos = meta_data(prog, filenames)
	format_name(dirpath, infos)

print("Done!")

