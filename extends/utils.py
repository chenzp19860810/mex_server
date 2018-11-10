# -*- coding: utf-8 -*-
# ------------Oooo---
# -----------(----)---
# ------------)--/----
# ------------(_/-
# ----oooO----
# ----(---)----
# -----\--(--
# ------\_)-
# ----
#     author : Yprisoner
#     email : yyprisoner@gmail.com
#                            ------
#    「 涙の雨が頬をたたくたびに美しく 」
import os
import time
import base64
import hashlib
import logging
import magneturi
import zipfile

logger = logging.getLogger(__name__)

"""
    常用工具
"""


def get_random_str():
    """
    获取唯一字符串
    :return:
    """
    md = hashlib.md5()
    md.update(bytes(str(time.time()) + ' | own-secret', encoding='utf-8'))
    return md.hexdigest()


def zip_file(input_path, out_path=None):
    """
    压缩文件
    :param input_path: 要压缩的文件夹或文件路径
    :param out_path: 压缩文件保存的目录
    :return:
    """
    if not out_path is None:
        if not os.path.exists(out_path):
            os.mkdir(out_path, 0o755)

        if os.path.isfile(input_path):
            # 如果是文件
            file_path, file_name = os.path.split(input_path)
            filename, ext = os.path.splitext(file_name)
            zip_file_save_name = filename + '_' + time.strftime("%Y%m%d%H%M%S",
                                                                time.localtime(int(time.time()))) + '.zip'
            file = zipfile.ZipFile(out_path + os.sep + zip_file_save_name, 'w', zipfile.ZIP_DEFLATED)
            file.write(input_path)
            file.close()
        elif os.path.isdir(input_path):
            # 如果是文件夹
            file_list = []
            get_zip_file(input_path, file_list)
            zip_file_save_name = 'backups_folder_' + time.strftime("%Y%m%d%H%M%S",
                                                                   time.localtime(int(time.time()))) + '.zip'
            file = zipfile.ZipFile(out_path + os.sep + zip_file_save_name, 'w', zipfile.ZIP_DEFLATED)
            for item in file_list:
                file.write(item)
            file.close()
        else:
            raise RuntimeError('压缩文件 Error  input_path 不正确  {0}'.format(input_path))
    else:
        raise RuntimeError('压缩文件 Error  input_path 不能为空')


def get_zip_file(input_path, result):
    """
    遍历文件夹
    这里供上面的压缩文件夹使用
    :param input_path:
    :param result:
    :return:
    """
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + os.sep + file):
            get_zip_file(input_path + os.sep + file, result)
        else:
            result.append(input_path + os.sep + file)


def getMd5File(file_path):
    """
    获取文件md5
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        md5obj = hashlib.md5()
        maxbuf = 8192
        f = open(file_path, 'rb')
        while True:
            buf = f.read(maxbuf)
            if not buf:
                break
            md5obj.update(buf)
        f.close()
        hash = md5obj.hexdigest()
        return str(hash).upper()
    return None


def time2str(timestamp):
    """
    将时间戳转换成制定合适的时间
    :param timestamp:
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(int(timestamp) / 1000)))


def str2time(strtime, length=10):
    """
    将指定格式字符串转换为时间戳
    :param strtime:
    :return:
    """
    timestamp = int(time.mktime(time.strptime(strtime, "%Y-%m-%d")))
    if length == 10:
        return timestamp
    else:
        return timestamp * 1000


def gettimestamp():
    """
    获取10位时间戳
    :return:
    """
    return int(int(time.time()))


def sha1_encrypt(str):
    """
    sha1 加密
    :param str:
    :return:
    """
    sha1 = hashlib.sha1()
    sha1.update(str.encode())
    return sha1.hexdigest()


def str2md5(inp):
    """
    md5 加密
    :param inp:
    :return:
    """
    return hashlib.md5(str(inp).encode(encoding='UTF-8')).hexdigest()


def str2base64(inp):
    """
    Base64 编码
    :param inp:
    :return:
    """
    result = base64.b64encode(bytes(str(inp), encoding="utf-8")).decode("utf-8")
    return result


def base642str(inp):
    """
    Base64反编码
    :param inp:
    :return:
    """
    result = base64.b64decode(inp)
    return str(result, encoding='UTF-8')



def getFileSize(file_path):
    """
    获取文件大小 MB
    方便文件上传
    :param file_path: 文件路径
    :return:
    """
    size = os.path.getsize(file_path)
    return round(size / 1024 / 1024, 2)



def image2base64(file):
    """
    图片转base64
    :param file: 可以是文件路径 也可以是二进制数据
    :return:
    """
    if isinstance(file, str) and os.path.isfile(file):
        return base64.b64encode(open(file, 'rb').read())
    else:
        try:
            return base64.b64encode(file)
        except Exception as e:
            raise TypeError('图片转base64 Error {0}'.format(e))



def file_get_contents(file_path):
    """
    获取文件内容
    命名来源php
    :param file_path: 文件路径
    :return: 文件内容
    """
    if os.path.isfile(file_path):
        with open(file_path, 'r+', encoding='UTF-8') as file:
            content = file.read()

        return content.strip()
    else:
        logger.error("{0}  不是文件".format(file_path))



def file_put_contents(file_path, content):
    """
    将内容写入文件
    命名来源php 习惯了
    :param file_path: 文件路径
    :param content: 要写入的内容
    :return:
    """
    file = open(file_path, 'w', encoding='UTF-8')
    try:
        file.write(content)
    except Exception as e:
        logger.error("写入文件error [{0}]".format(e))
    finally:
        file.close()



def torrent2magnet_file(file_path):
    """
    种子转磁力
    种子文件转成磁力
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        mange_link = magneturi.from_torrent_file(file_path)
        mange_link = mange_link.replace('magnet:?xt=urn:btih:', '')
        mange_32hash = mange_link.split('&')[0]
        mange_16hash = base64.b16encode(base64.b32decode(mange_32hash))
        mange_info = str(mange_16hash.lower(), encoding="utf-8")
        return "magnet:?xt=urn:btih:%s" % mange_info
    else:
        raise TypeError("种子转磁力 文件不存在 ~")



def torrent2magnet_contents(file_contents=None):
    """
    种子转磁力
    通过文件内容转为磁力 (不用保存种子文件通过requests返回直接转磁力)
    :param file_contents: requests 返回的 content 或者 open 方式打开
    :return:
    """
    if file_contents:
        mange_link = magneturi.from_torrent_data(file_contents)
        mange_link = mange_link.replace('magnet:?xt=urn:btih:', '')
        mange_32hash = mange_link.split('&')[0]
        mange_16hash = base64.b16encode(base64.b32decode(mange_32hash))
        mange_info = str(mange_16hash.lower(), encoding="utf-8")
        return "magnet:?xt=urn:btih:%s" % mange_info
    else:
        raise TypeError("种子转磁力 内容不为空 ~")
