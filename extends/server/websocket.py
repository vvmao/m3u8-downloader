# !/usr/bin/env python3
# -*- coding:utf-8 -*-


import json
from extends.server.websocket_server import WebsocketServer
from extends.Config.config import Config
from extends.downloader.manage import Manage


class Server(WebsocketServer):
    callMethod = {}

    def __init__(self):
        self.config = Config.getInstance()
        self.manage = Manage(Server)
        super(Server, self).__init__(self.config.get('websocket.port'), self.config.get('websocket.ip'))
        self.set_fn_new_client(self.new_client)
        self.set_fn_message_received(self.get_message)
        self.run_forever()

    def new_client(self, client, server):
        server.send_message(client, json.dumps({"status": "0", "type": "msg", "msg": "连接成功", "data": {}}))

    def get_message(self, client, server, message):
        """
        获得客户端的信息
        :param client:
        :param WebsocketServer server:
        :param message:
        :return:
        """
        try:
            data = json.loads(message)
            # server.send_message(client, data)
        except ValueError as e:
            data = {}
            pass
        if 'type' in data:
            if data['type'] == "cmd":
                data = getattr(self.manage, data['cmd'])(*data['args'])
                if data is None:
                    pass
                else:
                    server.send_message(client, json.dumps(data))
        else:
            server.send_message(client, json.dumps({"status": "10001", "type": "msg", "msg": "口令错误", "data": {}}))

    def stop(self):
        self.server_close()
