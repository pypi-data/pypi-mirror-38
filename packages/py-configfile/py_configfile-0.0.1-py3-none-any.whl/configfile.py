# -*- coding: utf-8 -*-
# Author: ZhangTianJie


import json
import os.path
import time

import yaml


class ConfigFile(object):
    """ 配置文件模块"""
    config_dir = os.path.abspath('')

    def is_app_exist(self, sign, suffix):
        """判断配置文件是否存在"""
        file_path = os.path.join(self.config_dir, '.'.join([sign, suffix]))
        if not os.path.isfile(file_path):
            return False
        else:
            return file_path

    def load_app(self, sign):
        """加载应用配置"""
        if self.is_app_exist(sign, 'yaml'):
            return self.load_app_yaml(sign)
        elif self.is_app_exist(sign, 'json'):
            return self.load_app_json(sign)
        return None

    @staticmethod
    def load_out(file_path):
        """加载外部配置文件"""
        suffix = file_path.split('.')[-1]
        method = 'load_out_' + suffix
        if hasattr(ConfigFile, method):
            return getattr(ConfigFile, method)(file_path)
        else:
            return False

    def load_app_json(self, sign):
        """加载应用配置文件"""
        file_path = self.is_app_exist(sign, 'json')
        return self.load_out_json(file_path)

    @staticmethod
    def load_out_json(file_path):
        """加载外部配置文件"""
        if not os.path.isfile(file_path):
            return False
        with open(file_path) as f:
            return json.loads(f.read())

    def load_dynamic_json(self, sign, callback, expires=3600):
        """动态加载配置文件"""
        file_path = self.is_app_exist(sign, 'dynamic.json')
        # 文件不存在处理
        if not file_path:
            file_path = os.path.join(self.config_dir, '.'.join([sign, 'dynamic', 'json']))
            with open(file_path, 'w') as f:
                f.write(callback())
        # 文件过期处理
        st_m_time = os.stat(file_path).st_mtime
        if time.time() > (st_m_time + expires):
            with open(file_path, 'w') as f:
                f.write(callback())
        # 文件正常处理
        return self.load_app_json(sign + '.dynamic')

    def load_app_yaml(self, sign):
        """加载应用配置文件"""
        file_path = self.is_app_exist(sign, 'yaml')
        return self.load_out_yaml(file_path)

    @staticmethod
    def load_out_yaml(file_path):
        """加载外部配置文件"""
        if not os.path.isfile(file_path):
            return False
        with open(file_path, 'rb') as f:
            return yaml.load(f.read())
