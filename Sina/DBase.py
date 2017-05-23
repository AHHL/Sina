#!/usr/bin/env python
# -*- coding: utf-8 -*-

# data=[{'a':2},{"b":3}]
# 插入文档
# db.checkin_info.insert(data)

from pymongo import MongoClient
from log import Logger

class ToMongo:
    def __init__(self):
        self.client = MongoClient('127.0.0.1', 27017)
        self.db = self.client.szpoi
        self.log=Logger().log()
    def InsertDoc(self, data):
        try:
            cursor = self.db.poiinfo.insert_many(data)
            self.client.close()

            return len(cursor.inserted_ids)
        except Exception as e:
            s='数据插入失败:%s' % e
            self.log.warning(s)
            return False

    def SearchCount(self):
        cursor = self.db.checkin_info2.count()
        return cursor
    def search(self):
        cursor = self.db.poiinfo.find()
        data=[]
        poi=[]
        for i in cursor:
            if i["city" ]=="0755"  and i["poiid"] not in poi:
                poi.append(i["poiid"])
                data.append(i)
        print len(poi)
        print len(data)
        cursor = self.db.poiinfo2.insert_many(data)
if __name__ == '__main__':
    m = ToMongo()
    m.search()
