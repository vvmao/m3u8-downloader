# !/usr/bin/env python36
from extends.Config.config import Config
from extends.downloader.interface import interface
import requests
import threading
import os
import json
import ssl
import platform
# from extends.db.sql import Task
from Crypto.Cipher import AES
import datetime
from time import sleep
from copy import deepcopy
import urllib3
from urllib.parse import urljoin

urllib3.disable_warnings()


class m3u8(interface):

    def __init__(self, uri, out_path, filename, manage, gid):
        self.thread_total: int = 0
        self.urlsbox: list = []
        self.key: str = ''
        self.urls: list = []
        self.isPause: bool = False
        self.isStop: bool = False
        self.slice = 100
        self.memory = {}
        self.sysstr = platform.system()
        super(m3u8, self).__init__(uri, out_path, filename, manage, gid)
        # self.db_task = Task()

    def setStatus(self, status):
        self.status = status
        # self.db_task.update_task(self.gid, self.status)

    def init(self):
        # self.db_task.create_task(
        #     {'task_id': self.gid, 'url': self.uri, 'filename': self.filename, 'file_path': self.out_path,
        #      'user_data': '', 'status': self.status, 'type': 'm3u8'})
        # ssl._create_default_https_context = ssl._create_unverified_context
        (self.tmp_path,) = os.path.join(Config.getInstance().APP_PATH, self.manage.getConfig('tmp_path'),
                                        datetime.datetime.now().strftime('%Y%m%d_%H%M%S')),
        self.setStatus(1)
        all_content = requests.get(self.uri, verify=False, timeout=(3, 7)).text  # 获取第一层M3U8文件内容
        if "#EXTM3U" not in all_content:
            self.setStatus(3)
        if "EXT-X-STREAM-INF" in all_content:  # 第一层
            file_line = all_content.split("\n")
            for line in file_line:
                if '.m3u8' in line:
                    url = urljoin(self.uri, line)
                    all_content = requests.get(url, verify=False, timeout=(3, 7)).text
                    file_line = all_content.split("\n")
                    self.urls = []
                    self.key = ''
                    for index, line in enumerate(file_line):  # 第二层
                        if "#EXT-X-KEY" in line:  # 找解密Key
                            method_pos = line.find("METHOD")
                            comma_pos = line.find(",")
                            method = line[method_pos:comma_pos].split('=')[1]

                            uri_pos = line.find("URI")
                            quotation_mark_pos = line.rfind('"')
                            key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

                            key_url = urljoin(url, key_path)  # 拼出key解密密钥URL
                            res = requests.get(key_url, verify=False, timeout=(3, 7))
                            self.key = res.content.decode()

                        if "EXTINF" in line:  # 找ts地址并下载
                            pd_url = urljoin(url, file_line[index + 1])  # 拼出ts片段的URL
                            self.urls.append(pd_url)
                    self.urlsbox = deepcopy(self.urls)
                    self.setStatus(2)
        elif "#EXT-X-VERSION" in all_content:
            url = self.uri
            all_content = requests.get(url, verify=False, timeout=(3, 7)).text
            file_line = all_content.split("\n")
            self.urls = []
            self.key = ''
            for index, line in enumerate(file_line):  # 第二层
                if "#EXT-X-KEY" in line:  # 找解密Key
                    method_pos = line.find("METHOD")
                    comma_pos = line.find(",")
                    method = line[method_pos:comma_pos].split('=')[1]

                    uri_pos = line.find("URI")
                    quotation_mark_pos = line.rfind('"')
                    key_path = line[uri_pos:quotation_mark_pos].split('"')[1]

                    key_url = urljoin(url, key_path)  # 拼出key解密密钥URL
                    res = requests.get(key_url, verify=False, timeout=(3, 7))
                    self.key = res.content.decode()

                if "EXTINF" in line:  # 找ts地址并下载
                    pd_url = urljoin(url, file_line[index + 1])  # 拼出ts片段的URL
                    self.urls.append(pd_url)
            self.urlsbox = deepcopy(self.urls)
            self.setStatus(2)

    def start(self):
        tmps = "%s/%s.json" % (os.path.join(Config.getInstance().APP_PATH, self.manage.getConfig('tmp_path')), self.gid)
        if os.path.exists(tmps):
            with open(tmps, 'r') as fp:
                self.urlsbox = json.load(fp)

        if self.status != 2 and self.status != 5:
            pass
        else:
            self.thread_total = 0
            self.setStatus(4)
            if not os.path.exists(self.tmp_path):
                os.makedirs(self.tmp_path)
            while True:
                if not self.isPause:
                    if len(self.urlsbox) == 0 and self.thread_total == 0:
                        break
                    if len(self.urlsbox) > 0 and self.thread_total < self.manage.getConfig('max_thread'):
                        url = self.urlsbox.pop(0)
                        index = self.urls.index(url)
                        t = threading.Thread(target=self.down,
                                             args=(url, self.tmp_path, index))
                        t.setDaemon(True)
                        t.start()
                        self.thread_total += 1
                if self.isStop:
                    break
                sleep(0.001)
            if not self.isStop:
                while True:
                    if self.thread_total == 0 and len(self.memory) == 0:
                        break
                    sleep(0.001)
                self.complate()
            else:
                while True:
                    if self.thread_total == 0 and len(self.memory) == 0:
                        break
                    sleep(0.001)
                self.clean()

    def __del__(self):
        if not self.isStop:
            tmps = "%s/%s.json" % (
                os.path.join(Config.getInstance().APP_PATH, self.manage.getConfig('tmp_path')), self.gid)
            if os.path.exists(tmps):
                with open(tmps, 'w') as fp:
                    self.urlsbox = json.load(fp)

    def save(self):
        tmps = "%s/%s.json" % (os.path.join(Config.getInstance().APP_PATH, self.manage.getConfig('tmp_path')), self.gid)
        if os.path.exists(tmps):
            with open(tmps, 'w') as fp:
                self.urlsbox = json.load(fp)

    def clean(self):
        if self.sysstr == 'Windows':
            os.system("rmdir /s /q %s" % self.tmp_path)
        else:
            os.system("rm -rf %s" % self.tmp_path)

    def complate(self):
        if self.sysstr == 'Windows':
            file_path = os.path.join(self.out_path, self.filename)
            os.system('copy /b %s\*.ts %s' % (self.tmp_path, file_path))
            os.system("rmdir /s /q %s" % self.tmp_path)
        else:
            file_list = os.listdir(self.tmp_path)
            file_list.sort(key=lambda x: int(x[:-3]))
            file_path = os.path.join(self.out_path, self.filename)
            if not os.path.exists(self.out_path):
                os.makedirs(self.out_path)
            with open(file_path, 'wb+') as fhand:
                for i in range(len(file_list)):
                    fhand.write(open(os.path.join(self.tmp_path, file_list[i]), 'rb').read())
            os.system("rm -rf %s" % self.tmp_path)
        self.setStatus(6)

    def writeContent(self, index, tmp_path, content):
        key = index // self.slice
        key2 = index % self.slice
        max_key = (len(self.urls) - 1) // self.slice
        max_key2 = (len(self.urls) - 1) % self.slice
        if key not in self.memory:
            self.memory[key] = {}
        self.memory[key][key2] = content
        if key == max_key:
            if len(self.memory[key]) == max_key2 + 1:
                with open(os.path.join("%s/%06d.ts" % (tmp_path, key)), 'ab+') as f:
                    for x in range(max_key2 + 1):
                        f.write(self.memory[key].get(x))
                    del self.memory[key]
        elif len(self.memory[key]) == self.slice:
            with open(os.path.join("%s/%06d.ts" % (tmp_path, key)), 'ab+') as f:
                for x in range(self.slice):
                    f.write(self.memory[key].get(x))
                del self.memory[key]

    def down(self, url, tmp_path, index):
        try:
            res = requests.get(url, verify=False, timeout=(3, 7))
            if len(self.key):
                cryptor = AES.new(self.key, AES.MODE_CBC, self.key)
                content = cryptor.decrypt(res.content)
                if len(content):
                    self.writeContent(index, tmp_path, content)
                else:
                    self.urlsbox.append(url)
            else:
                if len(res.content):
                    self.writeContent(index, tmp_path, res.content)
                else:
                    self.urlsbox.append(url)

        except Exception as e:
            print(e)
            self.urlsbox.append(url)

        self.thread_total -= 1

    def getProcess(self, keys=[]):
        return {'gid': self.gid, 'totalLength': len(self.urls), "downloadSpeed": self.getDownloadsSpeed(),
                "status": self.status, "uri": self.uri, 'title': self.title, "thread_total": self.thread_total}

    def getDownloadsSpeed(self):
        if len(self.urls) == 0:
            return 0
        else:
            return (len(self.urls) - len(self.urlsbox) - self.thread_total) * 100 / len(self.urls)

    def pause(self):
        """
        暂停下载
        :return:
        """
        self.isPause = True
        self.setStatus(5)

    def stop(self):
        self.isStop = True
        sleep(1)
        while 1:
            if self.thread_total > 0:
                sleep(0.1)
            else:
                break
        os.system("rm -rf %s" % self.tmp_path)
        os.remove(
            "%s/%s.json" % (os.path.join(Config.getInstance().APP_PATH, self.manage.getConfig('tmp_path')), self.gid))
        self.manage._task.pop(self.gid)

    def unPause(self):
        self.isPause = False
        self.setStatus(4)


if __name__ == '__main__':
    d = m3u8("", "../down/", '', None)
