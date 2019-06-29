# !/usr/bin/env python36
import os

from extends.Config.config import Config
from extends.downloader.m3u8 import m3u8
from extends.downloader.interface import interface
import datetime


class Manage:
    """
    @extends.downloader.interface.Interface
    """
    _task = {}  # type:dict[int,interface]
    __Version = "1.0.0"
    __session = {"sessionId": ""}

    def __init__(self, server=None):
        self.server = server
        self.config = Config.getInstance()

    def getConfig(self, key):
        return self.config.get(key)

    def createTask(self, task: dict):
        gid: str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if 'outpath' not in task.keys():
            task['outpath'] = self.getConfig('default.download_path')
        task['outpath'] = os.path.join(self.config.APP_PATH, task['outpath'])
        self._task[gid] = m3u8(task['uri'], task['outpath'], task['filename'], self, gid)
        self._task[gid].init()
        self._task[gid].start()

    def addUri(self, uris=[], options={}, position={}):
        if len(uris) == 0:
            return ''
        else:
            pass

    def remove(self, gid):
        pass

    def pause(self, gid):
        self._task[gid].pause()

    def pauseAll(self):
        for (git, task) in self._task:
            task.pause()

    def getTaskList(self):
        data = []
        for gid, task in self._task.items():
            data.append(task.getProcess())
        return {"status": 0, "type": "getTaskList", "msg": "获取成功", "data": data}

    def unPause(self, gid):
        return self._task[gid].unPause()

    def unpauseAll(self):
        try:
            for gid, task in self._task.items():
                task.unPause()
            return 0
        except Exception as e:
            return e.messages

    def tellStatus(self, gid, keys: list) -> dict:
        return self._task[gid].getProcess(keys)

    def getUris(self, gid) -> dict:
        return {"uri": self._task[gid].uri, "statuc": self._task[gid].status}

    def getFiles(self, gid) -> list:
        return self._task[gid].getFiles()

    def getPeers(self, gid) -> dict:
        """
        仅限bt下载
        :param gid:
        :return:
        """
        data = {}
        return data

    def getServers(self, gid):
        return [{'index': 1, "servers": {"uri": "", "currentUri": "", "downloadSpeed": ""}}]

    def tellActive(self, keys):
        """
        此方法返回活动下载列表
        like tellStatus
        :param keys:
        :return:
        """
        return []

    def tellWaiting(self, offset, num, keys):
        """
        此方法返回等待下载列表
        :param keys:
        :return:
        """
        return []

    def tellStopped(self, offset, num, keys):
        """
        此方法返回已停止下载的列表
        :param keys:
        :return:
        """

    def changePosition(self, gid, pos: int, how: str):
        """

        :param gid:
        :param pos:
        :param how:str POS_SET POS_CUR POS_END
        :return:
        """
        return

    def changeUri(self, gid, fileIndex, delUris, addUris, position=[]):
        """

        :param gid:
        :param fileIndex:
        :param delUris:
        :param addUris:
        :param position:
        :return:
        """
        pass

    def getOption(self, gid):
        pass

    def changeOption(self):
        pass

    def getGlobalOption(self):
        pass

    def changeGlobalOption(self):
        pass

    def getGlobalStat(self):
        pass

    def purgeDownloadResult(self):
        pass

    def removeDownloadResult(self, gid):
        pass

    def getVersion(self):
        return self.__Version

    def getSessionInfo(self):
        return self.__session

    def shutdonw(self):
        pass

    def saveSession(self):
        with open(self.config.get("session.save"), "w+") as fp:
            fp.write(str(self.__session))
        for gid, task in self._task.items():
            task.save()
        return 'ok'

    def onDownloadStart(self):
        pass

    def onDownloadPause(self):
        pass

    def onDownloadComplete(self):
        pass

    def onDownloadError(self):
        pass

    def onBtDownloadComplete(self):
        pass

    def delTask(self, task_id):
        return self._task[task_id].stop()

    def getTask(self, task_id):
        pass


if __name__ == '__main__':
    m = Manage()
    # print(str(m))
    # m.createTask({"uri": "", "outpath": "../down/","filename": ""})
