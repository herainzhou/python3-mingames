#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
'''
python 爬虫小实战 ，爬 中国行政区域


整体思路，

网页地址
http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/index.html
1：获取到各省，代码名称 保存到mysql
2：再根据每个省去找下级，直到村或者社区


'''

import requests
from pyquery import PyQuery as pq
import datetime,time
import sys
from py_mysql_base import mysql_py
from bs4 import BeautifulSoup


class regionalism:
    hea = None
    url = None
    region_id = None
    _encoding = "gbk"
    html_tag = ('.provincetr a','.citytr a','.countytr a','.towntr a','.villagetr td')
    def __init__(self,config):
        self.hea = config['hea']
        self.url = config['url']

    # 获取省并保存
    def getprovince(self,args='index.html',parent_id=0,parent_tree='0,',region_level=0):
        req = requests.get(url=self.url+args,headers=self.hea)
        req.encoding=self._encoding
        html= req.text
        doc = pq(html)
        items = doc(self.html_tag[region_level]).items()
        son_id = []
        for tag in items:
            data = {'parent_id':parent_id,'parent_tree':parent_tree,'region_name':tag.text().strip(),'url':tag.attr('href'),'region_code':'','region_level':region_level}
            region_id = self.save(data)

    # 获取省下名并保存
    def getcity(self,args='index.html',parent_id=0,parent_tree='0,',region_level=0,depth=""):
        req = requests.get(url=self.url+args,headers=self.hea)
        req.encoding=self._encoding
        html= req.text
        doc = pq(html)
        items = doc(self.html_tag[region_level]).items()
        i=0
        j=0
        son_id = []
        for tag in items:
            if i%2 == 0:
                # 插入
                data = {'parent_id':parent_id,'parent_tree':parent_tree,'url':depth+tag.attr('href'),'region_code':tag.text().strip(),'region_level':region_level}
                self.region_id = self.save(data)
                j+=1

            else:
                # 更新
                data = {'region_name':tag.text().strip()}
                where = {'id':self.region_id}
                self.save(data,'update',where)
            i += 1

    # 获取村名并保存
    def getvillagetr(self,args='index.html',parent_id=0,parent_tree='0,',region_level=0):
        req = requests.get(url=self.url+args,headers=self.hea)
        req.encoding=self._encoding
        html= req.text
        doc = pq(html)
        items = doc(self.html_tag[region_level]).text()

        villagetr = items.split()
        sons = self.list_of_groups(villagetr,3)
        j=0
        for i in sons:
            del i[1]
            i.append(parent_id)
            i.append(parent_tree)
            i.append(region_level)
            sons[j] = tuple(i)
            j+=1
        if sons:
            conn = mysql_py()
            sql = "INSERT INTO py_region(region_code,region_name,parent_id,parent_tree,region_level) values(%s,%s,%s,%s,%s)"
            conn.exec_txsql(sql,sons)
            return conn.get_lastrowid()

    # 获取省下名并保存
    def getupatecity(self,args='index.html',region_id=0,region_code=0):
        req = requests.get(url=self.url+args,headers=self.hea)
        req.encoding=self._encoding
        html= req.text
        doc = pq(html)
        items = doc(self.html_tag[3]).items()
        i=0
        j=0
        son_id = []

        self.region_id = 0
        for tag in items:
            print(tag)
            if i%2 == 0:
                # 插入
                #data = {'parent_id':parent_id,'parent_tree':parent_tree,'url':depth+tag.attr('href'),'region_code':tag.text().strip(),'region_level':region_level}
                #self.region_id = self.save(data)
                if tag.text().strip() == region_code:
                    self.region_id = region_id
                else:
                    self.region_id = 0
                j+=1

            else:
                # 更新
                data = {'region_name':tag.text().strip()}
                where = {'id':self.region_id}
                if self.region_id > 0:
                    self.save(data,'update',where)
            i += 1
    # 获取村名并保存
    def getupdatevillagetr(self,args='index.html',region_id=0,region_code=0):
        req = requests.get(url=self.url+args,headers=self.hea)
        req.encoding=self._encoding
        html= req.text
        doc = pq(html)
        items = doc(self.html_tag[4]).text()

        villagetr = items.split()
        sons = self.list_of_groups(villagetr,3)
        j=0
        for i in sons:

            if i[0] == region_code:
                region_name = i[2]
                data = {'region_name':region_name}
                where = {'id':region_id}
                if region_id > 0:
                    self.save(data,'update',where)

            j+=1

    # 把一个打列表，转成多个小列表
    def list_of_groups(self,init_list, children_list_len):
        list_of_groups = zip(*(iter(init_list),) *children_list_len)
        end_list = [list(i) for i in list_of_groups]
        count = len(init_list) % children_list_len
        end_list.append(init_list[-count:]) if count !=0 else end_list
        return end_list

    # 保存到 mysql 返回最后一条插入id
    def save(self,data,method="insert",where={}):
        #print(data)
        table = 'py_region'
        conn = mysql_py()
        conn.auto_joint_sql(table,data,method,where)
        return conn.get_lastrowid()

    # 获取数据
    def getall(self,sql):
        conn = mysql_py()
        return conn.exec_selectsql(sql)


hea = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        ,'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        ,'Upgrade-Insecure-Requests' : '1'
        ,'Cookie': '_trs_uv=ju86r9pl_6_jr96; AD_RS_COOKIE=20082855; wzws_cid=9a23141ff81e503e1efe059ed5970f69eb1ef38c35494ec9912d65cc7f88da2cb166f888993547778d32a7666feff04ad18a53a8e82de43d2fcc8ac3e258d7ac'
        }
config = {'hea':hea,'url':'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/'}
reg = regionalism(config);
#reg.getprovince()
# 获取省级数据，再往下调用
#sql = "SELECT * FROM `py_region` WHERE region_level=3 and id > 40958 ORDER BY id asc "
sql = "SELECT d.region_name, c.region_name, b.region_name, a.region_code, a.id, a.region_name, b.url FROM py_region a LEFT JOIN py_region b ON b.id = a.parent_id LEFT JOIN py_region c ON c.id = b.parent_id LEFT JOIN py_region d ON d.id = c.parent_id WHERE FIND_IN_SET( a.id, '589997,566881,553587,300399,299837,299444,299146,298971,297905,297779,297453,296892,296827,296794,296783,296520,296476,296475,296292,295859,295755,295723,295637,295492,295354,295348,295323,295315,295266,295237,295183,294846,294776,294675,294674,294209,293783,293731,293647,293618,293609,293577,293487,293425,293305,293071,293053,293052,292934,292893,292888,292430,292103,292079,291661,291555,291548,291546,291541,291539,291429,291227,291218,291046,291045,290880,290770,290477,290331,290166,289921,289914,289906,289903,289880,289853,289841,289840,289814,289806,289768,289762,289760,289731,289722,289718,289345,289235,289191,289176,289079,289059,289046,288977,288890,288794,288759,288751,288750,288477,288392,288384,288358,287920,287907,287784,287704,287653,287652,287567,287335,287109,287067,286819,286797,286794,286776,286012,285982,285945,285934,285923,285887,285476,285396,285394,284519,284518,284497,284491,284485,284472,284468,284464,284458,284448,284447,284433,284323,284314,284313,284309,284296,284285,284230,284169,284102,284064,284056,284020,283626,283621,283593,283500,283382,283337,282861,282769,281816,281568,281364,281268,281264,281138,281100,280866,280597,280459,280425,280422,280387,280378,280345,280328,280306,280304,280270,280001,279961,279896,279566,279230,279213,279206,279145,279143,279121,279097,278801,278713,278711,278689,278644,278628,278536,278523,278170,278080,278028,277940,277939,277936,277935,277897,277892,275323,275269,275121,275066,274614,274516,274337,274294,274201,273980,273877,273714,273662,273616,273586,273471,273456,273455,273376,273229,272893,272478,272309,272215,272151,272135,272115,272073,272057,271973,271964,271945,271812,271782,271736,271623,271528,271518,271511,271499,271492,271485,271433,271423,271400,271382,271349,271300,271240,271235,271197,271136,271116,270559,270550,270513,270508,270506,270505,270499,270460,270427,270409,270301,270001,269998,269863,269604,269599,269591,269570,269553,269223,269078,269041,268834,268803,268566,268543,268048,267814,267813,267745,267744,267743,267690,267586,267583,267526,267480,267412,267406,267360,267304,267225,267196,267118,267108,267107,267101,267068,267039,267038,267013,267011,266996,266875,266737,266729,266642,266291,266165,265991,265819,265662,265610,265563,265557,265551,265524,222074,222064,222033,222005,221952,221941,221915,221911,221908,221894,221886,221883,221869,221864,221842,221837,221834,221813,221810,221796,221752,221751,221709,221686,221682,221664,221657,221636,221607,221594,221593,221566,221560,221557,221535,221534,221527,221510,221509,221499,221445,221427,221395,221364,221251,221246,221237,221106,221103,221099,221092,221090,221085,221078,221075,221063,221061,221045,221016,221015,221014,220944,220928,220912,220905,220882,220881,220880,220869,220838,220739,220736,220707,220700,220686,220652,220640,220638,220635,220628,220606,220581,220572,220571,220566,220565,220480,220427,220402,220377,220367,219903,219467,219345,219324,219163,218961,218960,218940,218731,218586,218537,218532,218487,218405,218370,218344,218256,218253,218097,218021,217962,217959,217910,217844,217661,217618,217612,216663,216645,216101,216067,215957,215225,215224,214800,212714,212670,212395,209580,209018,209017,207064,205492,202837,202820,202756,202506,202457,202021,201077,201065,200660,200602,200104,200070,200028,198673,198145,197506,197278,197165,196586,196506,196247,194350,194329,194326,194270,194158,194004,193460,193178,183389,177010,176994,173648,169855,169806,168441,166822,165349,164428,164394,164303,164163,164111,164088,163792,163760,163749,160855,160359,160320,159969,159941,159851,158213,157880,151631,151374,151369,49902,46506');"
res = reg.getall(sql)
for g in res:
    print(g)
    reg.getupdatevillagetr(g[6],g[4],g[3])
    print("***************完结****************")
    #flag = reg.getupatecity(g[4],g[0],g[2]+str(g[0])+',',g[6]+1)
    #print(flag)
    #time.sleep(15)


exit()








