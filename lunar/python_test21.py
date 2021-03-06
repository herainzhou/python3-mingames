#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
'''
输入年月日时，输出8字

理论基础
年份
方法2：求 某年的年干支 ： （当年年数-3）% 60 余数为所求年干支的代数，再到六十环周图中找出相应的干支
方法2： ['庚','辛','壬','癸','甲','乙','丙','丁','戊','己'] 下标与年份尾数相对应
        ['申','酉','戌','亥','子','丑','寅','卯','辰','巳','午','未'] 下标与年份%12相对应


月份
方法： 歌诀
甲己之年丙作首，乙庚之岁戊为头，
丙辛之岁庚寅上，丁壬壬寅顺行流，
若言戊癸何方起，甲寅之上去寻求。

日干支
方法1 ：已知 某年元旦干支，该年推算日干日支
公式： 日干代数 = 元旦天干代数+所求日数±按月加减数-天干周转数。
    日支代数 = 元旦地支代数+所求日数±按月加减数-地支周转数。

说明：1：按月加减数是根基日数与六十环周推算出来的。
    2：各月干支加减表如下图

    | 月份 |  1月  |  2月  |  3月  | 4月  |  5月  |  6月  |  7月  | 8月  |  9月  |  10月 |  11月 | 12月  |
    | 干支 | 干|支 | 干 |支 | 干|支 | 干|支 | 干|支 | 干|支 | 干|支 | 干|支 | 干|支 | 干|支 | 干|支 | 干|支 |
    | 平年 | -1|-1 | +0|-6 | -2|+10| -1|+5 | -1|-1| +0|+6 | 0|0  | +1|+7 | +2|+2 | +2|+8 | +3|+3| +3|+9 |
    | 闰年 | 0|0   | 0 |0  |                               +1                                           |

    举例： 已知 1981 年元旦干支为 "乙卯"， 求该年 8月 14日干支
    解答：1981 年为平年 推算日干支代数，
    日干代数 = 己6+14+1-（前面相加数%10）*10 = 1 （甲）
    日支代数 = 卯4+14+7-（前面相加数%12）*12 = 1 （子）
    故1981年8月14日的日干支为 甲子

方法二：已知某年元旦干支，推求所求年的元旦干支，再推求该年的日干支
公式： 1平年求下一年的元旦干支=平年的元旦干支的基数+5
    （因为平年的元旦到下一年的元旦，干支数差5天）
    2闰年求下一年的元旦干支= 闰年的元旦干支的基数+6
    （因为平年的元旦到下一年的元旦，干支数差6天）
举例：已知 1980 年的元旦干支是癸酉，求1981年的元旦干支。
解答：1980 年为闰年，推算日干支代数，
    日干代数 = 癸10+6-10 = 6（己）
    日支代数 = 酉10+6-12 = 4（卯）
    故 1981 年的元旦干支为己卯

方法3：已知某年某日的日干支，求该年或他年的日干支
步骤：①先求日总数
    ②总数的个位数（个位为0则取10），作为顺数日干的根据，按值顺数即为所求日支；
    ③总数与12取余（能整除则取12），作为顺数日支的根据，按值顺数即为所求日支
举例： 已知1988 年元月4日为 戊午 求 1988 年 8月 23日干支。
解答：1）求日总数
    元月  2月  3月  4月  5月 6月 7月 8月
    28 +  29 + 31 + 30 + 31+ 30+31+23 = 233 天
    2）总数个位数推日干
    个位是3 。从 戊推 戊->己->庚 故日干为庚
    3）总数%12 推日支
    233 %12 = 5 从午推 ，午->未->申->酉->戌，故日支为戌
    故8月23日干支为庚戌

方法4 ：高氏日柱公式
 r = s/4*6+5(s/4*3 + u) + m + d + x

 符合意义：
 r: 日柱的母数 ，r%60 即是日柱的干支序数
 s: 公元年数后两位数减1，取整数值
 u: s%4
 m: 月基数
 d: 日期数
 x: 世纪常数
 注意 闰年 2月之后，求出的r需要再加上1
 其中 月基数 以及世纪常数分别为：
月基数：
月份：  | 1 | 2  | 3  | 4  | 5 | 6  | 7 | 8  | 9 | 10 | 11 | 12 |
月基数：| 0 | 31 | -1 | 30 | 0 | 31 | 1 | 32 | 3 | 33 | 4  | 34 |

世纪常数：
世纪数：  | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
世纪常数：| 3  | 47 | 31 | 15 | 0  | 44 | 28 | 12 | 57 | 41 |

例子：
2006 年 4 月 1 日 的干支纪日
s : 06 - 1 = 5
u : 5%4 = 1
m : 30
d : 1
x : 0

得 5//4*6 + 5x(5//4*3 + 1) + 30 + 1 + 0 = 6+5*4+31 = 57  57%10 = 7 -> 庚  57%12 = 9 -> 申    即 庚申日



备注： 元月  2月  3月   4月   5月   6月   7月   8月   9月  10月   11月   12月
平年    31   28   31   30    31    30    31    31   30    31     30     31
闰年        29


时干支的计算方法
方法：每日十二时辰与十二地支相配是固定不变的，因一天起于夜半的子时，故计算时亦从子时起，然后即顺排下去即值一天的时辰干支，有日上起时歌诀如下
甲己还加甲，乙庚丙作初，丙辛生戌子，
丁壬庚子头，戊癸起壬子，周而复始求。

甲己起甲子：甲日，己日夜半的子时起于甲子时，顺推乙丑
乙庚起丙子：乙日，庚日夜半的子时起于丙子时，顺推丁丑
丙辛起戊子：丙日，辛日夜半的子时起于戊子时，顺推己丑
丁壬起庚子：丁日，壬日夜半的子时起于庚子时，顺推辛丑
戊癸起壬子：戊日，癸日夜半的子时起于壬子时，顺推癸丑



算二十四节气
二十四节气表 ["立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
            "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
            "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
            "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]
方法： 计算公式：[Y*D+C]-L
每个世纪都有一个 C值
Y：年数后两位
D：常数 0.2422
C：世纪值
L：闰年数

21世纪，各个节气对应的常数C
[3.87, 18.73, 5.63, 20.646, 4.81, 20.1, 5.52, 21.04, 5.678, 21.37, 7.108, 22.83, 7.5, 23.13, 7.646, 23.042, 8.318, 23.438, 7.438, 22.36, 7.18, 21.94, 5.4055, 20.12]

20世纪 各个节气对应的常数C
[4.6295,19.4599,6.3826,21.4155,5.59,20.888,6.318,21.86,6.5,22.2,7.928,23.65,8.35,
23.95,8.44,23.822,9.098,24.218,8.218,23.08,7.9,22.6,6.11,20.84]

例外：
1：2026年计算得出的         雨水 日期应调减一天
2：2084年计算得出的         春分 日期加一天
3：1911年计算得出的         立夏 日期加一天
4：2008年计算得出的         小满 日期加一天
5：1902年计算得出的         芒种 日期加一天
6：1928年计算得出的         夏至 日期加一天
7：1925年和2016年计算得出的 小暑 日期加一天
8：1922年计算得出的         大暑 日期加一天
9：2002年计算得出的         立秋 日期加一天
10:1927年计算得出的         白露 日期加一天
11:1942年计算得出的         秋分 日期加一天
12:2089年计算得出的         霜降 日期加一天
13:2089年计算得出的         立冬 日期加一天
14:1978年计算得出的         小雪 日期加一天
15:1954年计算得出的         大雪 日期加一天
16:1918年和2021年计算得出的 冬至 日期减一天
17:1982年计算得出小寒日期加一天 2019 年 减一天
18:2082年计算得出的         大寒 日期加一天

备注：
一月 寅月     二月 卯月     三月 辰月  四月 巳月
从立春到惊蛰 从惊蛰到清明 从清明到立夏 从立夏到芒种
五月 午月     六月 未月    七月 申月  八月 酉月
从芒种到小暑 从小暑到立秋 从立秋到白露 从白露到寒露
 九月 戌月    十月 亥月    十一月 子月  十二月 丑月
从寒露到立冬 从立冬到大雪 从大雪到小寒 从小寒到立春



五行： 金木水火土
相生： 木生火  火生土  土生金  金生水  水生木
相克： 木克土  土克水  水克火  火克金  金克木

与天干地支的关系
金： 庚 辛 申 酉       西    秋
木： 甲 乙 寅 卯       东    春
水： 壬 癸 亥 子       北    冬
火： 丙 丁 巳 午       南    夏
土： 戊 己 辰 未 戌 丑  中   四季最后一个月

当令者旺，我生者相，生我者休，克我者困，我克者死

壬申年 辛亥月 壬辰日 甲辰时
水金   金水    水土  木土


癸酉年 乙卯月 辛卯日 己丑时
水金   木木   金木   土土


'''