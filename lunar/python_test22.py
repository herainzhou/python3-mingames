#!/usr/bin/python3.7
# -*- coding:utf-8 -*-

'''
整体思路
1：根据公式算出节气日期 1900 年到 2100  200 年的时间
2：特殊的年份进行纠正
3：保存到文件里去


'''
import sys
import json
import gc

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)

# 读取年份为 name 年的节气数据
def read_json_file(name):
    json_file = open('./json/' + name + '.json', 'r')
    json_str = json_file.read()
    dic = json.loads(json_str)
    print(dic)

# 读取测试
# read_json_file('2029')

# 读取所有年份的节气数据
def check_all_file():
    for index in range(2000, 2100):
        c_file_name = './json/{0}.json'.format(str(index))
        json_file = open(c_file_name, 'r')
        json_str = json_file.read()
        dic = json.loads(json_str)
        print (str(index) + dic)

# 计算节气的C常量组
C_list_21 = [3.87, 18.73, 5.63, 20.646, 4.81, 20.1, 5.52, 21.04, 5.678, 21.37, 7.108, 22.83, 7.5, 23.13, 7.646, 23.042, 8.318, 23.438, 7.438, 22.36, 7.18, 21.94, 5.4055, 20.12]

C_list_20 = [4.6295, 19.4599, 6.3826, 21.4155, 5.59,20.888, 6.318, 21.86, 6.5, 22.2, 7.928, 23.65, 8.35,  23.95, 8.44, 23.822, 9.098, 24.218, 8.218, 23.08, 7.9, 22.6, 6.11, 20.84]

# 节气名称组
name_Arr = ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]

#循环100年，计算节气日期，并创建文件
def creat_all_year():
    # type: () -> null
    for year in range(00, 99):
        list_arr = []
        for i in range(0, 24):
            C = C_list_21[i]
            ## 注意：凡闰年3月1日前闰年数要减一，即：L=[(Y-1)/4],因为小寒、大寒、立春、雨水这两个节气都小于3月1日,所以 y = y-1
            if i == 0 or 1 or 10 or 11:
                days = (year * 0.2422 + C) // 1 - ((year - 1) // 4)
            else:
                days = (year * 0.2422 + C) // 1 - (year // 4)
            days = int(days)
            days = '%02d' % days
            y = int(year // 1)
            m = i // 2 + 2
            if m == 13:
                m = 1
            m = '%02d' % m
            y = '%02d' % y
            strs = "20{0}-{1}-{2} 00:00:00".format(str(y), str(m), str(days))
            item = dict(name=name_Arr[i], jieqiid=str(i + 1), time=strs)
            # print (item)
            list_arr.append(item)
        print(list_arr)
        list_str = json.dumps(list_arr)
        # file_name = "./json/20{0}.json".format(str(year))
        # with open(file_name, "w") as f:
        #     json.dump(list_str, f)
        #     print("20{0}已载入文件完成...".format(str(year)))

creat_all_year()