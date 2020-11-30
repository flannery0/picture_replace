#!/bin/python
#coding=gbk

import io
import os
import re
file_path = "./"

url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
patten = b">\s+"
patten_2 = b"\s+<"
def alter(file,old_str,new_str):
    with io.open(file, "rb") as f:
        file_data = f.read()
        file_data = file_data.replace(old_str,new_str)
        file_data = file_data.replace(b"  ",b"")
        file_data = re.sub(patten,b">",file_data)
        file_data = re.sub(patten_2,b"<",file_data)
    with io.open(file,"wb") as f:
        f.write(file_data)

g = os.walk(file_path)  

for path,dir_list,file_list in g: 
    for file_name in file_list: 
        print("replace ", file_name) 
        alter(file_name,b"\n",b"")
