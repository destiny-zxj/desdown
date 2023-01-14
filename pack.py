#!/usr/bin/env python3
"""
将已命名软件包重新打包
"""
import re
import sys
import os
import time
import shutil

temp_dir = ".temp"


def print_exit(msg: str = None, code=0):
    # shutil.rmtree(temp_dir)
    if msg is not None and msg != "":
        print(msg)
    sys.exit(code)


def pack(info: dict, raw_filename: str):
    filename = "{}_{}_{}_{}".format(info['name'], info['version'], info['platform'], info['arch'])
    app_format = info['format']
    decompress = filename
    if app_format.find("tar.gz") != -1:
        app_format = "tar.gz"
        decompress = "tar xvf {} -C .temp".format(raw_filename)
    elif app_format.find("zip") != -1:
        app_format = "zip"
        decompress = "unzip {}".format(raw_filename)
    else:
        print_exit("不支持的文件格式")
    print("解压文件: {}".format(raw_filename))
    status = os.system(decompress)
    if status != 0:
        print_exit("解压出错！")
    print(filename, raw_filename)
    # print(status)


def run():
    raw_filename = "resources/alist_3.8.0_darwin_amd64.tar.gz"
    if not os.path.exists(raw_filename):
        print_exit("指定文件不存在: {}".format(raw_filename))
    filename = os.path.basename(raw_filename)
    print(filename)
    l_filename = filename.lower()
    pattern = re.compile(r'[a-zA-Z]+_([0-9]\.){2}[0-9]_[a-z]+_[a-z]+.+')  # 生成一个正则表达式对象
    res = pattern.search(l_filename)
    if res is None:
        print_exit("请按照格式命名软件包！(详情查看 `README.md` -> `软件包名详解`)")
    params = l_filename.split("_")
    if params[-1].find(".") != -1:
        temp = params[-1]
        params[-1] = temp[:temp.find(".")]
        params.append(temp[temp.find("."):])
    if len(params) != 5:
        print_exit("请按照格式命名软件包！(详情查看 `README.md` -> `软件包名详解`)")
    info = {
        'name': params[0],
        'version': params[1],
        'platform': params[2],
        'arch': params[3],
        'format': params[4]
    }
    print("软件包命名检查通过！")
    time.sleep(0.5)
    print("正在打包 ...")
    pack(info, raw_filename)


if __name__ == '__main__':
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    args = sys.argv
    run()
    print_exit()
