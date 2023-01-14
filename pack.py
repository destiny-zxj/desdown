#!/usr/bin/env python3
"""
将已命名软件包重新打包
  ./pack.py resources/name_x.x.x_platform_arch.tar.gz
  python3 pack.py resources/name_x.x.x_platform_arch.tar.gz
"""
import re
import sys
import os
import time
import shutil
from util import Util

temp_dir = ".temp"
is_clean_origin = False


def print_exit(msg: str = None, code=0):
    global temp_dir
    shutil.rmtree(temp_dir)
    if msg is not None and msg != "":
        print(msg)
    sys.exit(code)


def un_pack(info: dict, raw_filename: str) -> tuple:
    global temp_dir
    filename = "{}_{}_{}_{}".format(info['name'], info['version'], info['platform'], info['arch'])
    app_format = info['format']
    decompress = filename
    if app_format.find("tar.gz") != -1:
        app_format = "tar.gz"
        decompress = "tar xvf {} -C {}".format(raw_filename, temp_dir)
    elif app_format.find("zip") != -1:
        app_format = "zip"
        decompress = "unzip {}".format(raw_filename)
    else:
        print_exit("不支持的文件格式")
    print("解压文件: {}".format(raw_filename))
    status = os.system(decompress)
    if status != 0:
        print_exit("解压出错！")
    files = Util.get_files(temp_dir)
    bin_files = []
    conf_files = []
    service_files = []
    for file in files:
        if os.access(file, os.X_OK):
            bin_files.append(file)
            continue
        if file.find("conf") != -1:
            conf_files.append(file)
            continue
        if file.find("service") != -1:
            service_files.append(file)
            continue
    return bin_files, conf_files, service_files


def pack(info: dict, bin_files=None, conf_files=None, service_files=None):
    if service_files is None:
        service_files = []
    if conf_files is None:
        conf_files = []
    if bin_files is None:
        bin_files = []
    name = info['name']
    version = info['version']
    app_format = info['format']
    filename = "{}_{}_{}_{}".format(name, version, info['platform'], info['arch'])
    app_dir = os.path.join("software", name)
    version_dir = os.path.join(app_dir, version)
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
    if not os.path.exists(version_dir):
        os.mkdir(version_dir)
    if not os.path.exists(filename):
        os.mkdir(filename)
    if len(bin_files) > 0:
        dst_dir = os.path.join(filename, "bin")
        # os.mkdir(dst_dir)
        Util.move(bin_files, dst_dir)
    if len(conf_files) > 0:
        dst_dir = os.path.join(filename, "conf")
        # os.mkdir(dst_dir)
        Util.move(conf_files, dst_dir)
    if len(service_files) > 0:
        dst_dir = os.path.join(filename, "service")
        # os.mkdir(dst_dir)
        Util.move(service_files, dst_dir)
    decompress = filename
    package_name = filename + app_format
    if app_format.find("tar.gz") != -1:
        app_format = "tar.gz"
        decompress = "tar zcvf {} {}".format(package_name, filename)
    elif app_format.find("zip") != -1:
        app_format = "zip"
        decompress = "zip -rv {}".format(package_name)
    else:
        print_exit("不支持的文件格式")
    # print("压缩文件: {}".format(package_name))
    print("正在压缩...")
    status = os.system(decompress)
    if status != 0:
        print_exit("压缩出错！")
    shutil.rmtree(filename)
    Util.move(files=[package_name], dist=version_dir)
    print("压缩完成！")


def write_file(info: dict):
    print("更新文件...")
    name = info['name']
    version = info['version']
    app_dir = os.path.join("software", name)
    package_list_file = os.path.join(app_dir, "package.list")
    readme_file = os.path.join(app_dir, "readme.txt")
    # 写 package.list 文件
    print("  更新: {}".format(package_list_file))
    Util.append_to_file(package_list_file, version, version)
    time.sleep(0.5)
    readme_data = "\n".join([version, "Name: {}".format(name), "Version: {}".format(version), "end"])
    print("  更新: {}".format(readme_file))
    Util.append_to_file(readme_file, readme_data, version)
    time.sleep(0.5)
    print("文件更新完成！")


def run(raw_filename: str):
    global is_clean_origin
    if not os.path.exists(raw_filename):
        print_exit("文件不存在: {}".format(raw_filename))
    filename = os.path.basename(raw_filename)
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
    print("开始打包...")
    bin_files, conf_files, service_files = un_pack(info, raw_filename)
    pack(info, bin_files, conf_files, service_files)
    time.sleep(1)
    write_file(info)
    if is_clean_origin:
        print("正在清理...")
        print("  清理: {}".format(raw_filename))
        os.remove(raw_filename)
        print("清理完成！")
    print("打包完成！")


if __name__ == '__main__':
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    args = sys.argv
    if len(args) < 2:
        print_exit("请指定要打包的源安装包！")
    if args[-1] == '-d':
        is_clean_origin = True
    input_filename = args[1]
    run(raw_filename=input_filename)
    print_exit()
