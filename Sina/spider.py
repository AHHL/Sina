#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import math
from weibo import *
from log import Logger
import random
# 获取一个格网内的所有poi
class GetPOIs:
    # 获取当前时间
    def __init__(self,key,k):
        self.key=key
        self.k=k
        self.access_token=self.key[self.k]
        self.proxie={}
        self.log=Logger().log()

    def login(self):
        app_keys=["3561655282","2519129354","1943921431","1735592594"]
        app_secrets = ['f8ca52c67768125eba42b5bd98eb0cf6','b9a6c1d48f371803411d8f8e7bda870e','4bd7058772a64dfb2c315d9a289111e3','6e78c45787ba9fb80f55861003bd7282']
        call_back = "https://api.weibo.com/oauth2/default.html"
        num=random.randint(0,len(app_keys)-1)
        client = APIClient(app_key=app_keys[num], app_secret=app_secrets[num], redirect_uri=call_back)
        return client
    def get_pois(self,pois):
            length = len(pois)
            data = []

            for j in range(0, length):
                list = []
                poi = pois[j]
                if 'poiid' in poi:
                    list.append(poi['poiid'])
                    list.append(poi['title'])
                    list.append(poi['address'])
                    if 'phone' not in poi:
                        list.append('')
                    else:
                        list.append(poi['phone'])
                    list.append(poi['photo_num'])
                    if 'postcode' not in poi:
                        list.append('')
                    else:
                        list.append(poi['postcode'])
                    list.append(float(poi['lon']))
                    list.append(float(poi['lat']))
                    if 'city' in poi['district_info']:
                        list.append(poi['district_info']['city'])
                    else:
                        list.append('')
                    list.append(poi['city'])  # 城市代码
                    list.append(poi['category_name'])
                    if 'poi_pic' in poi:
                        list.append(poi['poi_pic'])
                    else:
                        list.append('')
                    list.append(int(poi['checkin_num']))  # 签到次数
                    list.append(int(poi['checkin_user_num']))  # 签到用户数
                    # 见该poi记录写入txt文件
                    # p=''
                    # for j in list:
                    #     if type(j) is unicode:
                    #         p = p + j.encode('utf-8') + '&'
                    #     else:
                    #         p = p + str(j) + '$'
                    # wstr = p[0:len(p) - 1] + '\n'
                    # f.write(wstr)
                    data.append(self.create_dict(list))
                else:
                    continue
            return data

    def create_dict(self,value):
        #构造一个poi的字典
        key=['poiid','title','address','phone','photo_num','postcode','lon','lat','district_info','city','category_name','poi_pic','checkin_num','checkin_user_num']
        poi_dict = dict(zip(key,value))
        return  poi_dict
    def place_nearby_pois(self,lat,long,radius,area_count):
        info='Start_Get第%d个格网数据开始获取: 经纬度:%f,%f.' % (area_count, lat, long)
        self.log.warning(info)
        start = time.clock()
        i = 1
        data = []  # 装载一个网格内的poi信息,可能包含很多页的数据
        while True:
            try:
                content = self.login().place.nearby.pois.get(access_token=self.access_token, lat=lat, long=long, range=radius, count=50,
                                                       page=i)
                if (len(content) == 0 or len(content["pois"]) == 0) and i == 1:
                    info='Empty第 %d 个格网没有数据' % area_count
                    self.log.warning(info)
                    data = []
                    return data
                if len(content)!= 0:
                    pois = content["pois"]
                    if len(pois)!=0:
                        total_number = content['total_number']  # poi总数
                        if total_number>=200:
                            #左上
                            lat1=lat+radius/2.0/110946.258
                            radius1=1.42*radius/2.0
                            long1=long-radius/2.0/111319.491
                            data1=self.place_nearby_pois(lat1,long1,radius1,area_count)
                            # 右上
                            lat2=lat+radius/2.0/110946.258
                            long2=long+radius/2.0/111319.491
                            radius2=1.42*radius/2.0
                            data2=self.place_nearby_pois(lat2,long2,radius2,area_count)
                            # 左下
                            radius3=1.42*radius/2.0
                            long3=long-radius/2.0/111319.491
                            lat3=lat-radius/2.0/110946.258
                            data3=self.place_nearby_pois(lat3,long3,radius3,area_count)
                            # 右下
                            radius4=1.42*radius/2.0
                            long4=long+radius/2.0/111319.491
                            lat4=lat-radius/2.0/110946.258
                            data4=self.place_nearby_pois(lat4,long4,radius4,area_count)
                            data=[]
                            for i in data1:
                                data.append(i)
                            for i in data2:
                                data.append(i)
                            for i in data3:
                                data.append(i)
                            for i in data4:
                                data.append(i)
                            return data

                        page_num = int(math.ceil(total_number / 50.0))
                        one_page_pois = self.get_pois(pois)  # 解析一页中的poi
                        for poi in one_page_pois:
                            data.append(poi)
                if (i >= page_num):
                    end = time.clock()
                    info='End_Get第 %d 个格网获取完毕,总共 %d 页,poi总数 %d.数据获取耗费时间:%f seconds\n' % (area_count, page_num, total_number, end - start)
                    self.log.warning(info)
                    return data
                i = i + 1  # 翻页
            except APIError as e:
                if e.error_code == 10022:
                    info='IP请求频次超过上限.'
                    self.log.warning(info)
                    time.sleep(1200)
                if e.error_code == 10023:
                    info = '请求频次超过上限.'
                    self.log.warning(info)
                    time.sleep(300)
                    if self.k == len(self.key)-1:
                        self.k = 0
                    else:
                        self.k = self.k + 1
                    self.access_token = self.key[self.k]
                    info = '第 %d 个账号.' % self.k
                    self.log.warning(info)
                if e.error_code==10006:
                    info = str(e.error_code)
                    self.log.warning(info)
                    time.sleep(10)
                    if self.k == len(self.key)-1:
                        self.k = 0
                    else:
                        self.k = self.k + 1
                continue
            except urllib2.URLError, e:
                info='URL错误:'+str(e)
                self.log.warning(info)
                continue


if __name__ == '__main__':
    getpois=GetPOIs()
    getpois.place_nearby_pois()