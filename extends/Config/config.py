# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import yaml
import os


class Config():
    default_data = {"websocket.port": 12543, "websocket.ip": "192.168.0.8"}
    data = {}
    Intance = None
    APP_PATH = '.'

    def __init__(self):
        self.APP_PATH = os.getcwd()
        data = self.readConfig()
        self.data.update(self.default_data)
        self.data.update(data)

    @classmethod
    def getInstance(cls):
        if cls.Intance is None:
            cls.Intance = cls()
        return cls.Intance

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value

    def readConfig(self):
        with open(os.path.join(self.APP_PATH, 'config.yaml'), encoding="UTF-8") as fp:
            data = yaml.full_load(fp)
        return data

    def reload(self):
        data = self.readConfig()
        self.data = self.default_data.update(data)


if __name__ == '__main__':
    config = Config.getInstance()
    print(config.data)
