# -*- coding: utf-8 -*-
import os
import shutil



def copy_and_zip(file_list, dst_folder_name):
    '''
    批量复制文件到指定文件夹，然后把指定文件夹的内容压缩成ZIP并且删掉该文件夹
    :param file_list: 文件或文件夹
    :param dst_folder_name: 目标压缩文件的名称
    :return: 返回压缩文件路径
    '''
    for item in file_list:
        copy_file(item, dst_folder_name)
    # 这里我把输出文件的路径选到了程序根目录下
    source = os.getcwd() + "\\" + dst_folder_name
    shutil.make_archive(source, "zip", source)
    shutil.rmtree(source)
    return  os.path.join( os.getcwd(), "report.zip")


def copy_file(srcfile, filename):
    '''
    把文件或文件夹复制到指定目录中
    :param srcfile: 文件或者文件夹的绝对路径
    :param filename: 指定目录
    :return:
    '''
    dstfile = os.path.abspath(os.getcwd())
    # 这里我把输出文件的路径选到了程序根目录下
    folder_name = dstfile + "\\" + filename + "\\"
    if not os.path.isfile(srcfile):
        last_name = os.path.basename(srcfile)
        destination_name = folder_name + last_name
        shutil.copytree(srcfile, destination_name)
        print("copy %s -> %s" % (srcfile, destination_name))
    else:
        fpath, fname = os.path.split(folder_name)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copy2(srcfile, folder_name)  # 移动文件
        print("copy %s -> %s" % (srcfile, folder_name))


if __name__ == '__main__':

    file1 = r"E:\project\trade-auto\air_case\summary.html"
    file2 = r"E:\\project\\trade-auto\\air_case\\log"
    file3 = r"E:\\project\\trade-auto\\air_case\\report"
    file_list = [file2, file1, file3]
    # 目标压缩包名
    folder_name = "1234567"
    t = copy_and_zip(file_list, folder_name)
    print(t)