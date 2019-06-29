# !/usr/bin/nev python3
# -*- coding:utf-8 -*-

import atexit
import getopt
import os
import sys
import signal

from extends.Config.config import Config
from extends.server.websocket import Server


class Progess():
    pidFile: str

    def __init__(self):
        self.server = None
        if self.pidFile == '':
            print('config is error, miss pidFile')
            sys.exit(0)
        else:
            if os.path.exists(self.pidFile):
                with open(self.pidFile, 'r') as pfp:
                    self.pid = int(pfp.read())
            else:
                self.pid = 0

    def run(self):
        pass

    def deamon(self):
        pid = os.fork()
        if pid == -1:
            print("初始化失败")
        elif not pid == 0:
            sys.exit(0)
        else:
            os.chdir('/')
            os.umask(0)
            os.setsid()
            _pid = os.fork()
            if _pid == -1:
                print("初始化失败")
            elif not _pid == 0:
                sys.exit(0)
            else:
                sys.stdout.flush()
                sys.stderr.flush()
                with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
                    os.dup2(read_null.fileno(), sys.stdin.fileno())
                    os.dup2(write_null.fileno(), sys.stdout.fileno())
                    os.dup2(write_null.fileno(), sys.stderr.fileno())
                self.createPid()

    def createPid(self):
        self.pid = os.getpid()
        if self.pidFile:
            with open(self.pidFile, 'w+') as f:
                f.write(str(os.getpid()))
            # 注册退出函数，进程异常退出时移除pid文件
            atexit.register(os.remove, self.pidFile)

    def stop(self):
        if self.pid == 0:
            print("进程不在运行")
        else:
            os.kill(self.pid, signal.SIGKILL)
            os.remove(self.pidFile)
            self.pid = 0

    def start(self):
        if self.pid == 0:
            self.deamon()
            self.run()
        else:
            print("progess is runing ,pid: %s" % self.pid)

    def restart(self):
        self.stop()
        self.start()

    def reload(self):
        pass


class serverProgess(Progess):
    pidFile = '/run/m3u8_donwnloader.pid'

    def run(self):
        self.server = Server()


def usage():
    pass


if __name__ == '__main__':
    config = Config.getInstance()
    p = serverProgess()
    try:
        options, args = getopt.getopt(sys.argv[1:], "d:", [])
    except getopt.GetoptError:
        sys.exit()
    if len(args) > 0 and len(options) == 0:
        print("参数错误")
    else:
        if len(options) == 0:
            p.start()
        for name, value in options:
            if name == "-d":
                getattr(p, value)()
