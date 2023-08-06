import json
import os
import urllib.parse
import platform
import random
from .time_plus import DatetimePlus

class FuncHelper(object):
    # 字典转JSON
    @staticmethod
    def dict_to_json(dValue, ensure_ascii=False):
        return json.dumps(dValue, ensure_ascii=False)

    # JSON转字典
    @staticmethod
    def json_to_dict(jValue):
        return json.loads(jValue)

    # 创建目录树
    @staticmethod
    def create_dirs(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    #生成一个DJANGO上传目录在STATIC下的
    @staticmethod
    def get_static_upload_path():
        sysstr = platform.system()
        path = os.getcwd()
        if sysstr.lower() == 'windows':
            path += '\\static\\upload\\' + DatetimePlus.get_now_datetime_to_filename_month()
        else:
            path += '/static/upload/' + DatetimePlus.get_now_datetime_to_filename_month()
        return path

    # 从URL返回文件名
    @staticmethod
    def get_file_name_by_url(url=''):
        i = url.rfind('/') + 1
        return url[i:]

    # 获取扩展名
    @staticmethod
    def get_file_extname(s=''):
        i = s.rfind('.') + 1
        return s[i:]

    @staticmethod
    def get_file_name_no_extname(file_name):
        i = file_name.rfind('.') + 1
        return file_name[:i - 1]

    # 返回程序根目录
    @staticmethod
    def get_curr_path():
        return os.getcwd()

    @staticmethod
    def get_dirs_name_by_path(path):
        result = []
        if not FuncHelper.check_directory_exists(path):
            return result
        for dirpath, dirnames, filenames in os.walk(path):
            for dir in dirnames:
                result.append(dir)
            break
        return result

    @staticmethod
    def get_files_name_by_path(path):
        result = []
        if not FuncHelper.check_directory_exists(path):
            return result
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                result.append(file)
            break
        return result

    @staticmethod
    def get_file_name_by_all_path(path):
        return path[path.rfind('/'):]

    # 字典转实例 用于向JS中访问JSON那样用.方法
    @staticmethod
    def dict_to_instance(data):
        if not isinstance(data, dict):
            return None
        result = type('myInstance', (), data)
        for key in data.keys():
            if isinstance(data[key], dict):
                setattr(result, key, FuncHelper.dict_to_instance(data[key]))
            elif isinstance(data[key], list):
                for i, d in enumerate(data[key]):
                    if isinstance(d, dict):
                        data[key][i] = FuncHelper.dict_to_instance(d)
        return result

    # JSON转实例 用于向JS中访问JSON那样用.方法
    @staticmethod
    def json_to_instance(jsonValue):
        jsonDict = FuncHelper.json_to_dict(jsonValue)
        return FuncHelper.dict_to_instance(jsonDict)

    # 检查文件是否存在
    @staticmethod
    def check_file_exists(filePath=''):
        return os.path.exists(filePath)

    # 检查文件夹是否存在
    @staticmethod
    def check_directory_exists(dirPath=''):
        return os.path.isdir(dirPath)

    @staticmethod
    def bytes_str_decode_str(s):
        try:
            result = s.decode(encoding="utf-8")
        except:
            result = ''
        return result

    # 检查文件夹是否存在
    @staticmethod
    def get_file_path_by_full_path(full_path=''):
        return full_path[:full_path.rfind('/')]  # 不包括/

    # 生产一个随机字符串
    @staticmethod
    def get_random_str(size=10,only_num=False,only_str=False):
        if only_num:
            s = '0123456789'
        elif only_str:
            s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        else:
            s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        if len(s) > size:
            result = random.sample(s,size)
        else:
            result = ''
            for i in range(size):
                result += random.choice(s)
        return result

    @staticmethod
    def get_module_name_by_path(path=''):
        module_name = path[1:]
        module_name = module_name[:module_name.find('/')]
        return module_name

    @staticmethod
    def get_all_classname_by_file_path_name(file_path_name, base_class_name='Base'):
        result = []
        if not FuncHelper.check_file_exists(file_path_name):
            return result
        with open(file_path_name, 'r',encoding='utf8') as f:
            for line in f.readlines():
                if line.startswith('class'):
                    _base_class_name = line[line.find('(') + 1:line.find(')')]
                    if _base_class_name == base_class_name:
                        result.append(line[6:line.find('(')])
        return result

    @staticmethod
    def quote(url):
        return urllib.parse.quote(url)

    @staticmethod
    def unquote(url):
        return urllib.parse.unquote(url)

    @staticmethod
    def urlencode(dict_):
        return urllib.parse.urlencode(dict_)

    @staticmethod
    def urldecode(params=''):
        params = params.split('&')
        data_dict = {}
        for _params in params:
            key = _params[:_params.find('=')]
            value = _params[_params.find('=') + 1:]
            data_dict[key] = value
        return data_dict

    @staticmethod
    def check_os_is_windows():
        return platform.system().lower() == 'windows'

    @staticmethod
    def cp_django_model_instance(instance, exclude_field=[]):
        if not instance:
            return None
        from django.db.models.query_utils import DeferredAttribute
        class_ = instance.__class__
        conpents = dir(class_)
        new_instance = class_()
        for c in conpents:
            if c.startswith('_'):
                continue
            v = getattr(class_, c)
            if isinstance(v, DeferredAttribute) and not c in exclude_field:
                setattr(new_instance, c, getattr(instance, c))
        return new_instance

    @staticmethod
    def get_tmp_path():
        sysstr = platform.system()
        if sysstr.lower() == 'windows':
            filename = os.environ["TMP"] + '\\'
        else:
            filename = '/tmp/'

        return filename

if __name__ == '__main__':
    # print( FuncHelper.getFileNameByUrl('http://www.evun.cc/adfklsdfjsdf/sdf/123456789.zip'))
    # print(FuncHelper.getCurrPath())
    pass