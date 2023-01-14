"""
工具类
"""
import os


class Util:
    """
    工具类
    """

    @staticmethod
    def get_files(dir_path: str) -> list:
        """
        遍历目录
        :param dir_path:
        :return:
        """
        out_files = []
        if not os.path.exists(dir_path):
            print('目录不存在！')
            return out_files
        if not os.path.exists(dir_path):
            return out_files
        files = os.listdir(dir_path)
        for i in range(len(files)):
            file = files[i]
            file_name = os.path.join(dir_path, file)
            if file.find('._') != -1 or file.find('.DS') != -1:
                continue
            if os.path.isdir(file_name):
                out_files.extend(Util.get_files(file_name))
            else:
                out_files.append(file_name)
        return out_files

    @staticmethod
    def move(files: list, dist: str):
        if not os.path.exists(dist):
            os.makedirs(dist)
        for file in files:
            if not os.path.exists(file):
                continue
            basename = os.path.basename(file)
            dst_name = os.path.join(dist, basename)
            os.rename(file, dst_name)
            print("Move: {} -> {}".format(file, dst_name))

    @staticmethod
    def append_to_file(filename: str, data: str, flag=None):
        """
        将文本数据写入文件。不存在则创建，存在则添加到头部

        :param filename:
        :param data:
        :param flag: 不可写标志。如果标志在行首找到则不可写
        :return:
        """
        can_write = False
        fpr_data = ""
        if not os.path.exists(filename):
            can_write = True
        else:
            with open(filename, mode='r', encoding='utf-8') as fpr:
                lines = fpr.readlines()
            if len(lines) <= 0:
                can_write = True
            if flag is not None and flag != "":
                found = False
                for line in lines:
                    if line.find(flag) == 0:
                        found = True
                        break
                can_write = not found
            if flag is None:
                can_write = True
            fpr_data = "".join(lines)
        if can_write:
            with open(filename, mode='w+', encoding='utf-8') as fpw:
                fpw.write("{}\n{}".format(data, fpr_data))
