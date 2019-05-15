#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
'''
输入年月日时，输出8字
'''
import time
import json
import sys
import os
import sxtwl

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)

class bazi:
    tiangan = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']
    dizhi   = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥']
    ShX     = ['鼠','牛','虎','兔','龙','蛇','马','羊','猴','鸡','狗','猪']
    ymc     = [u"十一", u"十二", u"正", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九", u"十" ]
    rmc     = [u"初一", u"初二", u"初三", u"初四", u"初五", u"初六", u"初七", u"初八", u"初九", u"初十",u"十一", u"十二", u"十三", u"十四", u"十五", u"十六", u"十七", u"十八", u"十九",u"二十", u"廿一", u"廿二", u"廿三", u"廿四", u"廿五", u"廿六", u"廿七", u"廿八", u"廿九", u"三十", u"卅一"]
    y_t = None  ## 年天干下标
    d_t = None  ## 日天干下标
    century = None  # 世纪数
    month = None # 所求月份
    year = None # 所求年份
    day = None # 所求日子
    hour = None # 所求时间
    is_run = None # 是否是闰年
    # 算年柱
    def getyear(self,year):
        # 算法： 年份 - 3 % 10 即天干对应的位置
        #        年份 - 3 % 12 即地支对应的位置
        self.y_t = (year-3)%10-1
        y_tian = self.tiangan[self.y_t]
        y_di = self.dizhi[(year-3)%12-1]

        return y_tian+y_di+"("+self.ShX[(year-3)%12-1]+')'+"年"

    # 算 月柱
    def getmonth(self,month):
        '''
        甲己之年丙作首，乙庚之岁戊为头，
        丙辛之岁庚寅上，丁壬壬寅顺行流，
        若言戊癸何方起，甲寅之上去寻求。
        '''
        yt_start = [2,4,6,8,0,2,4,6,8,0]
        tian_index = (yt_start[self.y_t] + int(month-1))%10
        m_tian = self.tiangan[tian_index]
        m_di = self.dizhi[(month+1)%12]
        return m_tian+m_di+"月"

    # 算日柱
    def getday(self,day):
        '''
        高氏公式  r = s//4*6+5(s//4*3 + u) + m + d + x
        r: 日柱的母数 ，r%60 即是日柱的干支序数
        s: 公元年数后两位数减1，取整数值
        u: s%4
        m: 月基数
        d: 日期数
        x: 世纪常数
        世纪常数公式  x = (44(c-17) + (c-17)//4 + 3)%60
        c : 世纪数

        注意 闰年 2月之后，求出的r需要再加上1
        月基数：
        月份：  | 1 | 2  | 3  | 4  | 5 | 6  | 7 | 8  | 9 | 10 | 11 | 12 |
        月基数：| 0 | 31 | -1 | 30 | 0 | 31 | 1 | 32 | 3 | 33 | 4  | 34 |

        世纪常数：
        世纪数：  | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
        世纪常数：| 3  | 47 | 31 | 15 | 0  | 44 | 28 | 12 | 57 | 41 |
        '''
        month_base = [0 , 31 , -1 , 30 , 0 , 31 , 1 , 32 , 3 , 33 , 4  , 34]
        century_base = [-3  , 47 , 31 , 15 , 0  , 44 , 28 , 12 , 57 , 41]
        s = self.year%100-1
        u = s%4
        m = month_base[self.month-1]
        x = (44 * (self.century-17)+ (self.century-17)//4 + 3)%60
        r = s//4*6+5*(s//4*3 + u) + m + day + x
        if self.is_run :
            if self.month > 2:
                r += 1
        self.d_t = r%10-1
        d_tian = self.tiangan[r%10-1]
        d_id = self.dizhi[r%12-1]

        return d_tian+d_id+"日"

    # 算时柱
    def gethour(self,hour):
        hours = [23,1,3,5,7,9,11,13,15,17,19,21]
        j = 1
        for i in hours:
            if hour >= i:
                h_di = j
            j += 1
        if h_di >= 11 :
            if hour >= hours[0]:
                h_di = 1
        '''
        甲己还加甲，乙庚丙作初，丙辛生戌子，
        丁壬庚子头，戊癸起壬子，周而复始求。
        '''
        ht_start = [0,2,4,6,8,0,2,4,6,8]
        h_index = (ht_start[self.d_t] + int(h_di-1))%10
        h_tian = self.tiangan[h_index]
        h_di = self.dizhi[h_di-1]
        return h_tian+h_di+"时"


    # 总方法
    def getbazi(self,datetime,is_Lunar=False):
        date = time.strptime(datetime, '%Y-%m-%d %H:%M:%S')
        unix_time = time.mktime(date)
        data = time.localtime(unix_time)
        note = "阳历"+datetime+" 的八字为 "
        if is_Lunar:
            note = "农历"+time.strftime('%Y',data)+"年"+self.ymc[(int(time.strftime('%m',data))+1)%12] + "月" + self.rmc[int(time.strftime('%d',data))-1] + " " + time.strftime('%H',data)+'点'+time.strftime('%M',data)+'分'+time.strftime('%S',data) + '秒 的八字為 '
            ## 农历转阳历
            lunar = sxtwl.Lunar()  #实例化日历库
            day = lunar.getDayByLunar(int(time.strftime('%Y',data)), int(time.strftime('%m',data)), int(time.strftime('%d',data)))
            datetime = str(day.y)+'-'+str(day.m)+'-'+str(day.d)+' '+time.strftime('%H',data)+':'+time.strftime('%M',data)+':'+time.strftime('%S',data)
            date = time.strptime(datetime, '%Y-%m-%d %H:%M:%S')
            unix_time = time.mktime(date)
            data = time.localtime(unix_time)

        self.year = int(time.strftime('%Y',data))

        ## 要加上24节气的判断，来确定所属月份
        jieqi = self.read_json_file(str(self.year))
        jieqi = json.loads(jieqi)
        newmonths = jieqi[::2]
        j = 1
        for i in newmonths:
            jqtime = int(time.mktime(time.strptime(i['time'], '%Y-%m-%d %H:%M:%S')))
            if j < 12:
                if int(unix_time) >= jqtime:
                    newmonth = j
            else:
                if int(unix_time) < jqtime:
                    newmonth = j
            j += 1

        self.month = int(time.strftime('%m',data))
        self.day = int(time.strftime('%d',data))
        self.hour = int(time.strftime('%H',data))
        self.century = self.year//100+1
        self.is_run = self.comrun(self.year)

        y = self.getyear(self.year)
        m = self.getmonth(newmonth)
        d = self.getday(self.day)
        h = self.gethour(self.hour)

        return note+y+m+d+h


    ## 算是否是闰年
    def comrun(self,year):
        i = 0
        if (year % 4) != 0 :
            i=0
        elif ((year % 100) == 0) & ((year % 400) != 0):
            i=0
        else:
            i=1
        return i

    ## 读取该年节气数
    def read_json_file(self,name):
        json_file = open('./json/' + name + '.json', 'r',encoding="utf-8")
        json_str = json_file.read()
        dic = json.loads(json_str)
        return dic

## 只能算 1970 年，到现在的年份的天干地支

if __name__ == '__main__':

    bz = bazi()
    print('************************欢迎进入洲洲算命程序**************************')
    print("请选择你输入的是农历还是阳历 1 阳历  2农历 ")
    result = 1
    while result == 1:
        flag = input("请输入1 or 2:")
        if flag.isdigit() :
            if int(flag) != 1 and int(flag) != 2 :
                print('请输入正确值')
                continue
        else:
            print('请输入正确值')
            continue
        result=2
    while result == 2:
        year = input("请输入年（范围 1970~2100）:")
        if year.isdigit() :
            if int(year) < 1970 :
                print('请输入正确的年份')
                continue
        else:
            print('请输入正确的年份')
            continue
        result=3
    while result == 3:
        month = input("请输入月（范围 1~12）:")
        if month.isdigit() :
            if int(month) < 1 or int(month) > 12 :
                print('请输入正确的月份')
                continue
        else:
            print('请输入正确的月份')
            continue
        result=4
    while result == 4:
        day = input("请输入日（范围 1~31）:")
        if day.isdigit() :
            if int(day) < 1 or int(day) > 31 :
                print('请输入正确的日子')
                continue
        else:
            print('请输入正确的日子')
            continue
        result=5
    while result == 5:
        hour = input("请输入时（范围 0~23）:")
        if hour.isdigit() :
            if int(hour) < 1 or int(hour) > 23 :
                print('请输入正确的小时')
                continue
        else:
            print('请输入正确的小时')
            continue
        result = 6


    datetime = year +'-'+month +'-'+ day +' '+hour+':00:00'

    if int(flag) == 1:
        is_Lunar = False
    else:
        is_Lunar = True

    res = bz.getbazi(datetime,is_Lunar)
    print('*****************结果**********************')
    print(res)
    print('*****************结束***********************')
    input('*****************恭喜了***********************')


