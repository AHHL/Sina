#!/usr/bin/env python
# -*- coding: utf-8 -*-
from spider import GetPOIs
from DBase import ToMongo
key=[]
with open("accessToken.txt") as f1:
    for i in f1:
        key.append(i.strip())
getpois=GetPOIs(key,0)
radius=3000
mydb=ToMongo()
from log import Logger
log=Logger().log()
with open('sz.txt','r') as f:
    for item in f:
        item=item.split(',')
        id=int(item[0])
        long=float(item[1])
        lat=float(item[2])
        data=getpois.place_nearby_pois(lat,long,radius,id)
        if len(data)!=0:
            row=mydb.InsertDoc(data)
            info="第%d个格网,共有%d条数据入库" % (id,len(data))
            log.warning(info)
f.close()