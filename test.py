# !/usr/bin/env python3
from extends.downloader.manage import Manage
from urllib.parse import urljoin
from urllib.parse import urlparse

if __name__ == '__main__':
    m = Manage(None)
    m.createTask({"uri": "", "filename": ""})
