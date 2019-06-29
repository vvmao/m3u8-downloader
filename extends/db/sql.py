#!/usr/bin/python3
# -*- coding:utf-8 -*-
import hashlib
import sqlite3


class Db(object):

    def __init__(self):
        self.conn = sqlite3.connect('./extends/db/downs.db')
        self.cursor = self.conn.cursor()

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            print("Reason:", e)
            self.conn.rollback()
            return False

    def add(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            print("Reason:", e)
            self.conn.rollback()
            return False

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            print("Reason:", e)
            self.conn.rollback()
            return False

    def select(self, sql):
        data = self.cursor.execute(sql)
        return data


class Task(Db):

    def create_task(self, data):
        sql = "INSERT INTO task(task_id,url,filename,file_path,user_data,status,type) VALUES(%s,'%s','%s','%s','%s',%s,'%s')" % (
            data['task_id'], data['url'], data['filename'], data['file_path'], data['user_data'], data['status'],
            data['type'])
        self.add(sql)

    def select_task(self):
        sql = "select task_id,url,filename,file_path,user_data,status,type from task"
        return self.select(sql)

    def check_task(self, url):
        sql = "select task_id from task where url = '%s'" %url
        return len(self.select(sql))

    def del_task(self, task_id):
        sql = "DELETE from task where task_id = %s" % task_id
        task_ext = Task_ext()
        task_ext.delete(task_id)
        return self.delete(sql)

    def update_task(self, task_id, status):
        sql = "update task set status  = %s where task_id = %s" % (status, task_id)
        self.update(sql)

    def __del__(self):
        self.conn.close()


class Task_ext(Db):
    def create_task(self, data):
        sql = "INSERT INTO task_ext(task_id,m3u8_file_1,m3u8_file_2,process_tmp_file) VALUES('%s','%s','%s','%s')" % (
            data['task_id'], data['m3u8_file_1'], data['m3u8_file_2'], data['process_tmp_file'])
        self.add(sql)

    def select_task(self):
        sql = "select task_id,m3u8_file_1,m3u8_file_2,process_tmp_file from task_ext"
        return self.select(sql)

    def del_task(self, task_id):
        sql = "DELETE from task_ext where task_id = %s" % task_id
        return self.delete(sql)


if __name__ == '__main__':
    pass
