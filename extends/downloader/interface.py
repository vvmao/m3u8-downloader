# !/usr/bin/env python36
import os.path


class interface():

    def __init__(self, uri, out_path, filename, manage, gid):
        self.process = 0
        """
        下载状态 0 未初始化 1 初始化中 2 初始化完成 3 初始化失败 4 下载中 5 下载暂停 6 下载完成 7 下载失败
        """
        self.status = 0
        self.uri = uri
        self.out_path = out_path
        fileinfo = os.path.splitext(filename)
        extension = filename[filename.rfind('.'):]
        fileTypes = [".3G2", ".3GP", ".3GP2", ".3GPP", ".AAC", ".AC3", ".AIFF", ".AMR", ".AMV", ".APE", ".ASF", ".ASS",
                     ".ASX", ".AVI", ".CDA", ".CUE", ".DIVX", ".DMSKM", ".DPG", ".DPL", ".DSF", ".DTS", ".DTSHD",
                     ".DVR", ".EAC3", ".EVO", ".F4V", ".FLAC", ".FLV", ".IDX", ".IFO", ".K3G", ".LMP4", ".M1A", ".M1V",
                     ".M2A", ".M2T", ".M2TS", ".M2V", ".M3U", ".M3U8", ".M4A", ".M4B", ".M4P", ".M4V", ".MKA", ".MKV",
                     ".MOD", ".MOV", ".MP2", ".MP2V", ".MP3", ".MP4", ".MPA", ".MPC", ".MPE", ".MPEG", ".MPG", ".MPL",
                     ".MPLS", ".MPV2", ".MQV", ".MTS", ".MXF", ".NSR", ".NSV", ".OGG", ".OGM", ".OGV", ".OPUS", ".PLS",
                     ".PSB", ".QT", ".RA", ".RAM", ".RM", ".RMVB", ".RPM", ".RT", ".SBV", ".SKM", ".SMI", ".SRT",
                     ".SSA", ".SSF", ".SUB", ".SUP", ".SWF", ".TAK", ".TP", ".TPR", ".TRP", ".TS", ".TTA", ".TTML",
                     ".USF", ".VOB", ".VTT", ".WAV", ".WAX", ".WEBM", ".WM", ".WMA", ".WMP", ".WMV", ".WMX", ".WTV",
                     ".WV", ".WVX", ".XSPF", ".XSS"]
        if fileTypes.count(extension.upper) == 0:
            self.filename = "%s.mp4" % filename
        self.title = filename
        self.manage = manage
        self.gid = gid

    def init(self):
        """
        初始化任务的方法
        :return:
        """
        pass

    def getProcess(self, keys=[]) -> dict:
        """
        获取下载进度及状态
        :return:dict [status,totalLength,completedLength,uploadLength,bitfield,downloadSpeed,uploadSpeed,infoHash,numSeeders,seeder,pieceLength,numPieces,connections,errorCode,errorMessage,followedBy,following,belongsTo,dir,files,bittorrent,verifiedLength,verifyIntegrityPending]
        """
        pass

    def pause(self):
        """
        暂停下载
        :return:
        """
        pass

    def delete(self):
        self.stop()
        return self.gid

    def stop(self):
        pass

    def start(self):
        """
        启动下载
        :return:
        """
        pass

    def unPause(self):
        pass

    def getFiles(self) -> list:
        """
        :return [{index,path,length,completedLength,selected,uris:{uri,status}}]:
        """
        file = [self.status]
        return file

    def save(self):
        pass
