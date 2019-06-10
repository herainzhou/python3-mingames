# -*- coding: utf-8 -*-
# 导入我们需要用到的包
import pygame
import os


'''
中国象棋，开发思路 流程
1：先画网格
2：摆子
3：走子
4：判断胜负


细节思路：
1： 生成一个全盘棋的列表 None
2： 定义一个棋子类，生成所有的棋子，走法，棋规，
3： 判断是否将军或绝杀，每走一步都需要判断
4： 生成一个正被选中的棋子变量，然后鼠标点击的时候做判断，
5： 将/帅的走法判断思路，算出所有对方可过河的棋子的在将/帅府可行坐标点，然后应该判断，不能这里面的可行坐标点
6： 还差一个将帅不能见面的判断 2019-05-17 完成
7： 棋子走了一步之后，然后就再算一遍过河的棋子,判断是否将军，将军之后，判断是否绝杀
9： 判断是否结束的判断，如果是将军，必须要解将  未完成  2019-05-17 完成 2019-05-21
10： 增加走棋记录 （完成），好返回上一步，下一步 未完成，  显示后10步数
11： 判断绝杀，被将军的时候，判断是否还有解，这个需要遍历全部棋子的所有可能走法 未完成 2019-05-21
12： 还有一个翻转棋局的操作 未完成

 車将军 有三种解法 1 吃車   2 中间放一个棋子     3 走将帅
 馬将军 有三种解法 1 吃馬   2 压馬脚            3 走将帅
 炮将军           1 吃炮   2 中间空地放一个棋子  3 走将帅
 兵卒将军         1 吃 兵卒 2 走将帅





'''
# 初始化
pygame.init()

# 初始化 mixer (导入背景音乐)
pygame.mixer.init()
# 设置宽高
width= 72*10 ## 360
height= 72*11  # 396
grid_width= width // 10
side_width = 200
side_width1 = 200

black=(0,0,0)
red=(251,4,4)
blue=(0, 0, 255)
white=(255, 255, 255)

cheese_color_red = (251,4,5) # 红棋
cheese_color_blue = (7,79,247) # 当前选中的棋子颜色
cheese_color_black = (10,10,10) #  黑棋

# 加载背景图片
base_folder = os.path.dirname(__file__)
img_folder = os.path.join(base_folder,'images')
background_img=pygame.image.load(os.path.join(img_folder,'back.png'))

screen = pygame.display.set_mode((width+side_width+side_width1, height))
pygame.display.set_caption("中国象棋")

background = pygame.transform.scale(background_img, (width, height))
back_rect = background.get_rect()

def text_object(text, font,color):
    ## 渲染到画布
    textSurface = font.render(text, True , color)
    return textSurface,textSurface.get_rect()

#显示文字提示
def writeTxt(surf):
    # 从系统字体创建一个Font对象  pygame.font.SysFont
    n = 1
    mlist = ['九','八','七','六','五','四','三','二','一']
    for i in range(9):
        draw_txt(surf,str(n),(n*grid_width-5,10))
        n+=1

    m = 1
    for j in range(9):
        draw_txt(surf,mlist[j],(m*grid_width-9,height-grid_width+40))
        m+=1

    heght_han = (grid_width-35)//2
    draw_txt(surf,'楚',(2*grid_width-9,5*grid_width+heght_han),35,1)
    draw_txt(surf,'河',(3*grid_width+2,5*grid_width+heght_han),35,1)
    draw_txt(surf,'漢',(6*grid_width+9,5*grid_width+heght_han),35,1)
    draw_txt(surf,'界',(7*grid_width+11,5*grid_width+heght_han),35,1)


    draw_txt(surf,'黑方',(width+20,2*grid_width-10),35)
    draw_txt(surf,'红方',(width+20,7*grid_width-10),35,0,red)

def draw_cheese(surf,color,pos,txt):
    pygame.draw.circle(surf,(185,122,87),pos,32)
    pygame.draw.circle(surf,color,pos,24,1)
    pygame.draw.circle(surf,color,pos,32,1)
    draw_txt(surf,txt,(pos[0]-15,pos[1]-15),30,0,color)


def draw_txt(surf,txt,pos,size=22,flag=0,color=black):
    # 定义字体
    txtSize = pygame.font.SysFont('SimHei',size)
    # 定义文字
    textSurf,textRect = text_object(txt,txtSize,color)
    if flag == 1:
       textSurf = pygame.transform.rotate(textSurf,90)
    # 定义 摆放位置
    textRect = pos
    # 渲染到画布上 将一个图像绘制到另一个
    surf.blit(textSurf,textRect)




class cheese():
    # 设置棋子的走位，走法
    chlist = {1:'車',2:'馬',3:'象、相',4:'士、仕',5:'将、帅',6:'炮,砲',7:'卒、兵'}
    screen_cheeses_matrix = None # 整个棋盘
    cheeses_log_pos = [] # 每一步的棋子兑换位置，即走棋记录
    cheeses_log_note = [] # 每一步的棋子文字说明，即走棋记录
    cheeses_log_cheese = [] # 每一步的棋子变化，即走棋记录
    can_matrix = [] # 选中棋的可行位置列表（除将帅）
    forbidden_zone =[] # 将帅的禁止着法
    can_move =[] # 所有走法列表

    down_ident = 1 # 棋子的双方 1 红，2 黑棋
    is_down = 0 # 是否被点击选中，1是，0否
    down_pos = (0,0) # 被选中的位置
    down_cheese = None # 被选中的棋子  (棋子名称，棋子阵营，棋子类型)
    eat_cheese = None # 被走动的棋子

    # 将帅的位置，需要保持起来
    zhu_pos = [(9,4),(0,4)]
    zhu = [0,0] # 是否有将军
    note = "" # 提示文字
    is_dui = 0; # 是否将帅见面了 0 否 1 是
    is_over = 0; # 是否结束 1 是，0 否


    def __init__(self):
        pass

    # 鼠标按下进入方法
    # color_metrix 棋子列表
    # pos 当前鼠标按下的位置
    # curr_ident 当前下子的标识 1 红，2 黑棋
    def power_down(self,pos,curr_ident=1):
        #print(pos)
        if self.is_down == 0:
            # 未选中,判断是否有棋子在，没有棋子不做为，有就显示被选中状态 一人一步
            if self.down_ident == curr_ident and self.screen_cheeses_matrix[pos[0]][pos[1]] is not None and self.screen_cheeses_matrix[pos[0]][pos[1]][1] == curr_ident :
                self.is_down = 1
                self.down_pos = pos
                self.down_cheese = self.screen_cheeses_matrix[pos[0]][pos[1]]
                self.screen_cheeses_matrix[pos[0]][pos[1]] = (self.down_cheese[0],3,self.down_cheese[2],self.down_cheese[3],self.down_cheese[4])
                self.addgetpos(pos,self.down_cheese[2],self.down_ident)
        else:
            # 有被选中的棋子了，判断是否在可行范围内
            if pos in self.can_matrix:
                if self.down_cheese[2] == 5:
                    self.zhu_pos[curr_ident-1] = pos

                self.eat_cheese = self.screen_cheeses_matrix[pos[0]][pos[1]]
                self.screen_cheeses_matrix[pos[0]][pos[1]] = (self.down_cheese[0],self.down_cheese[1],self.down_cheese[2],pos,self.down_cheese[4])
                self.screen_cheeses_matrix[self.down_pos[0]][self.down_pos[1]] = None
                # 判断是否将军
                res = self.is_jiang(curr_ident)
                print('将判断返回值：',res)
                # res 返回值说明 1 被将军  2 将军 3 没事，4绝杀
                if res == 1 or self.is_dui == 1:
                    self.screen_cheeses_matrix[pos[0]][pos[1]] = self.eat_cheese
                    self.screen_cheeses_matrix[self.down_pos[0]][self.down_pos[1]] = (self.down_cheese[0],3,self.down_cheese[2],self.down_cheese[3],self.down_cheese[4])
                    self.note = "被将军" if res == 1 else "将帅见面"
                    self.is_dui = 0
                    res = 5
                elif res == 2:
                    self.note = "将军"
                elif res == 4:
                    self.is_over = 1
                    self.note = "绝杀"
                else:
                    self.note = ''
                if res == 2 or res == 3 or res == 4:
                    self.addlog(self.down_cheese,self.eat_cheese,self.down_pos,pos,curr_ident)
                    self.is_down=0
                    self.down_pos=(0,0)
                    self.down_ident = 1 if self.down_ident==2 else 2
                    self.can_matrix=[]
                    self.forbidden_zone=[]
                    self.can_move=[]

            elif self.screen_cheeses_matrix[pos[0]][pos[1]] == (self.down_cheese[0],3,self.down_cheese[2],self.down_cheese[3],self.down_cheese[4]):
                self.is_down=0
                self.down_pos=(0,0)
                self.screen_cheeses_matrix[pos[0]][pos[1]] = self.down_cheese
                self.down_ident = curr_ident
                self.can_matrix=[]
                self.forbidden_zone=[]
                self.can_move=[]
        return self.screen_cheeses_matrix

    # 增加行棋记录
    # cheese    棋子
    # down_pos  上个节点
    # pos       当前节点
    # ident     下棋手 1红，2黑
    def addlog(self,cheese,eat_cheese,down_pos,pos,ident):
        rlist = ['九','八','七','六','五','四','三','二','一']
        jlist = ['一','二','三','四','五','六','七','八','九']
        blist = ['1','2','3','4','5','6','7','8','9']
        if ident == 1:
            # 红方记录
            if down_pos[0] == pos[0]:
                note = "平"+rlist[pos[1]]
            elif down_pos[1] == pos[1]:
                if down_pos[0] > pos[0]:
                    note = "进"
                elif down_pos[0] < pos[0]:
                    note = "退"
                note = note+jlist[abs(down_pos[0]-pos[0])-1]
            else:
                if down_pos[0] > pos[0]:
                    note = "进"
                elif down_pos[0] < pos[0]:
                    note = "退"
                note = note+rlist[pos[1]]
            cheese_note = cheese[0]+rlist[down_pos[1]]+note
        else:
            # 黑方记录
            if down_pos[0] == pos[0]:
                note = "平"+blist[pos[1]]
            elif down_pos[1] == pos[1]:
                if down_pos[0] < pos[0]:
                    note = "进"
                elif down_pos[0] > pos[0]:
                    note = "退"
                note = note+blist[abs(down_pos[0]-pos[0])-1]
            else:
                if down_pos[0] < pos[0]:
                    note = "进"
                elif down_pos[0] > pos[0]:
                    note = "退"
                note = note+blist[pos[1]]
            cheese_note = cheese[0]+blist[down_pos[1]]+note
        self.cheeses_log_note.append(cheese_note)
        self.cheeses_log_pos.append((down_pos,pos))
        self.cheeses_log_cheese.append((cheese,eat_cheese))

    # 返回传入值的可供选点
    # params  pos 点击的点位坐标
    # params  cheesetype  棋子的类型 chlist
    # params  ident  黑 2 ，红 1
    # can_xia 该棋子可以下的坐标列表 只有 将帅才需要判断
    def addgetpos(self,pos,cheesetype,ident):
        self.can_matrix = []
        #print(self.screen_cheeses_matrix)
        if cheesetype == 1:
            self.ju(pos,ident)
        elif cheesetype == 2:
            self.ma(pos,ident)
        elif cheesetype == 3:
            self.xiang(pos,ident)
        elif cheesetype == 4:
            self.shi(pos,ident)
        elif cheesetype == 5:
            self.jiang(pos,ident)
        elif cheesetype == 6:
            self.pao(pos,ident)
        elif cheesetype == 7:
            self.bingzu(pos,ident)
        return self.can_matrix

    # 車走位
    # param pos 位置
    # param ident 下棋红黑 （1 红 2 黑）
    # param flag 类别 0 判断車走位加自身位 1 判断車控制位
    def ju(self,pos,ident,flag=0):
        #print('車的位置：',pos)
        ju_matrix = []
        move_matrix = []
        # 车走直线，判断
        # 判断右边，条件结束是 到边界 and 已经存在棋子，
        right = pos[1]+1
        while right < 9 and self.screen_cheeses_matrix[pos[0]][right] is None :
            ju_matrix.append((pos[0],right))
            right += 1
        if flag == 1:
            if right < 9 and (self.screen_cheeses_matrix[pos[0]][right])[1] == ident:
                ju_matrix.append((pos[0],right))
        else:
            if right < 9 and (self.screen_cheeses_matrix[pos[0]][right])[1] != ident:
                ju_matrix.append((pos[0],right))
        # 判断左边 条件 到边界，and  已经存在棋子
        left = pos[1]-1
        while left >= 0  and self.screen_cheeses_matrix[pos[0]][left] is None :
            ju_matrix.append((pos[0],left))
            left -= 1
        if flag == 1:
            if left >= 0 and (self.screen_cheeses_matrix[pos[0]][left])[1] == ident:
                ju_matrix.append((pos[0],left))
        else:
            if left >= 0 and (self.screen_cheeses_matrix[pos[0]][left])[1] != ident:
                ju_matrix.append((pos[0],left))

        # 判断上边 条件 到边界，and  已经存在棋子
        up = pos[0]-1
        while up >= 0 and self.screen_cheeses_matrix[up][pos[1]] is None:
            ju_matrix.append((up,pos[1]))
            up -= 1
        if flag == 1:
            if up >= 0 and (self.screen_cheeses_matrix[up][pos[1]])[1] == ident:
                ju_matrix.append((up,pos[1]))
        else:
            if up >= 0 and (self.screen_cheeses_matrix[up][pos[1]])[1] != ident:
                ju_matrix.append((up,pos[1]))

        # 判断下边 条件 到边界，and  已经存在棋子
        down = pos[0]+1
        while down < 10 and self.screen_cheeses_matrix[down][pos[1]] is None:
            ju_matrix.append((down,pos[1]))
            down += 1
        if flag == 1:
            if down < 10 and (self.screen_cheeses_matrix[down][pos[1]])[1] == ident:
                ju_matrix.append((down,pos[1]))
        else:
            if down < 10 and (self.screen_cheeses_matrix[down][pos[1]])[1] != ident:
                ju_matrix.append((down,pos[1]))

        if flag == 1:
            self.forbidden_zone += ju_matrix
        elif flag == 2:
            for n in ju_matrix:
                move_matrix.append((pos,n))
            self.can_move += move_matrix

        else:
            self.can_matrix += ju_matrix

    def ma(self,pos,ident,flag=0):
        # 馬走日 判断
        ma_pos = [(1,2),(-1,2),(1,-2),(-1,-2),(-2,1),(-2,-1),(2,1),(2,-1)]
        # 日子对顶角
        can_ma = []
        move_ma = []
        can_ma_pos = []
        for p in ma_pos:
            can_ma.append((pos[0]+p[0],pos[1]+p[1]))

        # 去除压脚的坐标点位,不在棋盘的点
        down = pos[0]+1
        if down < 9 and self.screen_cheeses_matrix[down][pos[1]] is None:
            can_ma_pos.append(can_ma[7])
            can_ma_pos.append(can_ma[6])
        up = pos[0]-1
        if up > 0 and self.screen_cheeses_matrix[up][pos[1]] is None:
            can_ma_pos.append(can_ma[5])
            can_ma_pos.append(can_ma[4])
        left = pos[1]-1
        if left > 0 and self.screen_cheeses_matrix[pos[0]][left] is None:
            can_ma_pos.append(can_ma[3])
            can_ma_pos.append(can_ma[2])
        right = pos[1]+1
        if right < 8 and self.screen_cheeses_matrix[pos[0]][right] is None:
            can_ma_pos.append(can_ma[1])
            can_ma_pos.append(can_ma[0])
        # 去除棋子是己方的点
        can_ma = can_ma_pos
        yu_ma = []
        for i in can_ma:
            # 在棋盘内，并且不为己方棋子
            if flag == 1:
                if self.screen_cheeses_matrix[i[0]][i[1]] is None or (self.screen_cheeses_matrix[i[0]][i[1]])[1] == ident:
                    yu_ma.append(i)
            else:
                if self.screen_cheeses_matrix[i[0]][i[1]] is None or (self.screen_cheeses_matrix[i[0]][i[1]])[1] != ident:
                    yu_ma.append(i)
        if flag == 1:
            self.forbidden_zone += yu_ma
        elif flag == 2:
            for n in yu_ma:
                move_ma.append((pos,n))
            self.can_move += move_ma

        else:
            self.can_matrix += yu_ma

    def xiang(self,pos,ident):
        move_xiang = []
        # 相、象 走田，且不过河
        if ident == 1:
            # 相
            #can_xiamg = [(9,2),(7,0),(5,2),(7,4),(5,6),(7,8),(9,6)]
            ya_xiang = [(pos[0]+1,pos[1]+1),(pos[0]-1,pos[1]+1),(pos[0]-1,pos[1]-1),(pos[0]+1,pos[1]-1)]
            curr_xiang = [(pos[0]+2,pos[1]+2),(pos[0]-2,pos[1]+2),(pos[0]-2,pos[1]-2),(pos[0]+2,pos[1]-2)]
            j = 0
            for i in ya_xiang:
                if (5 <= i[0] <= 9) and (0 <= i[1] <=8) and self.screen_cheeses_matrix[i[0]][i[1]] is None:
                    if self.screen_cheeses_matrix[curr_xiang[j][0]][curr_xiang[j][1]] is None or (self.screen_cheeses_matrix[curr_xiang[j][0]][curr_xiang[j][1]])[1] != ident:
                        self.can_matrix.append(curr_xiang[j])
                j += 1

        elif ident == 2:
            # 象
            #can_xiamg = [(0,2),(2,0),(4,2),(2,4),(4,6),(2,8),(0,6)]
            ya_xiang = [(pos[0]+1,pos[1]+1),(pos[0]-1,pos[1]+1),(pos[0]-1,pos[1]-1),(pos[0]+1,pos[1]-1)]
            curr_xiang = [(pos[0]+2,pos[1]+2),(pos[0]-2,pos[1]+2),(pos[0]-2,pos[1]-2),(pos[0]+2,pos[1]-2)]
            j = 0
            for i in ya_xiang:
                if (0 <= i[0] <= 4) and (0 <= i[1] <=8) and self.screen_cheeses_matrix[i[0]][i[1]] is None:
                    if self.screen_cheeses_matrix[curr_xiang[j][0]][curr_xiang[j][1]] is None or (self.screen_cheeses_matrix[curr_xiang[j][0]][curr_xiang[j][1]])[1] != ident:
                        self.can_matrix.append(curr_xiang[j])
                j += 1
        self.forbidden_zone += self.can_matrix
        for n in self.can_matrix:
            move_xiang.append((pos,n))
        self.can_move += move_xiang

    def shi(self,pos,ident):
        move_shi = []
        # 士、仕 走九宫对角
        if ident == 1:
            # 仕
            # can_shi = [(9,3),(9,5),(8,4),(7,3),(7,5)]
            curr_xiang = [(pos[0]+1,pos[1]+1),(pos[0]-1,pos[1]+1),(pos[0]-1,pos[1]-1),(pos[0]+1,pos[1]-1)]
            for i in curr_xiang:
                if (7 <= i[0] <= 9) and (3 <= i[1] <= 5) and (self.screen_cheeses_matrix[i[0]][i[1]] is None or (self.screen_cheeses_matrix[i[0]][i[1]])[1] != ident):
                    self.can_matrix.append(i)
        elif ident == 2:
            # 士
            # can_shi = [(0,3),(0,5),(1,4),(2,3),(2,5)]
            curr_xiang = [(pos[0]+1,pos[1]+1),(pos[0]-1,pos[1]+1),(pos[0]-1,pos[1]-1),(pos[0]+1,pos[1]-1)]
            for i in curr_xiang:
                if (0 <= i[0] <= 2) and (3 <= i[1] <= 5) and (self.screen_cheeses_matrix[i[0]][i[1]] is None or (self.screen_cheeses_matrix[i[0]][i[1]])[1] != ident):
                    self.can_matrix.append(i)
        self.forbidden_zone += self.can_matrix
        for n in self.can_matrix:
            move_shi.append((pos,n))
        self.can_move += move_shi

    def jiang(self,pos,ident):
        #
        self.forbidden(ident)
        # 将帅走九宫格
        if ident == 1:
            # 帅
            curr_shuai = [(pos[0]+1,pos[1]),(pos[0]-1,pos[1]),(pos[0],pos[1]-1),(pos[0],pos[1]+1)]
            for i in curr_shuai:
                if (7 <= i[0] <= 9) and (3 <= i[1] <= 5) and (self.screen_cheeses_matrix[i[0]][i[1]] is None or (self.screen_cheeses_matrix[i[0]][i[1]])[1] != ident):
                    if i not in self.forbidden_zone:
                        self.can_matrix.append(i)
        elif ident == 2:
            # 将
            curr_jiang = [(pos[0]+1,pos[1]),(pos[0]-1,pos[1]),(pos[0],pos[1]-1),(pos[0],pos[1]+1)]
            for i in curr_jiang:
                if (0 <= i[0] <= 2) and (3 <= i[1] <= 5) and (self.screen_cheeses_matrix[i[0]][i[1]] is None or (self.screen_cheeses_matrix[i[0]][i[1]])[1] != ident):
                    if i not in self.forbidden_zone:
                        self.can_matrix.append(i)

    def pao(self,pos,ident,flag=0):
        # 炮走直线，隔一个可以掉
        pao_matrix = []
        move_matrix = []
        pao_forbix = []
        # 判断右边，条件结束是 到边界 and 已经存在棋子 and 隔一个棋子之后的后一个棋子，
        right = pos[1]+1
        while right < 9 and self.screen_cheeses_matrix[pos[0]][right] is None :
            pao_matrix.append((pos[0],right))
            right += 1
        right = right+1
        while right < 9 :
            if flag == 1:
                if self.screen_cheeses_matrix[pos[0]][right] is None:
                    pao_forbix.append((pos[0],right))
                elif self.screen_cheeses_matrix[pos[0]][right] is not None:
                    pao_forbix.append((pos[0],right))
                    break
            else:
                if self.screen_cheeses_matrix[pos[0]][right] is not None and (self.screen_cheeses_matrix[pos[0]][right])[1] != ident :
                    pao_matrix.append((pos[0],right))
                    break
            right += 1
        # 判断左边，条件结束是 到边界 and 已经存在棋子 and 隔一个棋子之后的后一个棋子，
        left = pos[1]-1
        while left >= 0 and self.screen_cheeses_matrix[pos[0]][left] is None :
            pao_matrix.append((pos[0],left))
            left -= 1
        left = left-1
        while left >= 0 :
            if flag == 1:
                if self.screen_cheeses_matrix[pos[0]][left] is None:
                    pao_forbix.append((pos[0],left))
                elif self.screen_cheeses_matrix[pos[0]][left] is not None:
                    pao_forbix.append((pos[0],left))
                    break
            else:
                if self.screen_cheeses_matrix[pos[0]][left] is not None and (self.screen_cheeses_matrix[pos[0]][left])[1] != ident :
                    pao_matrix.append((pos[0],left))
                    break
            left -= 1
        # 判断上边，条件结束是 到边界 and 已经存在棋子 and 隔一个棋子之后的后一个棋子，
        up = pos[0]-1
        while up >= 0 and self.screen_cheeses_matrix[up][pos[1]] is None :
            pao_matrix.append((up,pos[1]))
            up -= 1
        up = up-1
        while up >= 0 :
            if flag == 1:
                if self.screen_cheeses_matrix[up][pos[1]] is None:
                    pao_forbix.append((up,pos[1]))
                elif self.screen_cheeses_matrix[up][pos[1]] is not None:
                    pao_forbix.append((up,pos[1]))
                    break
            else:
                if self.screen_cheeses_matrix[up][pos[1]] is not None and (self.screen_cheeses_matrix[up][pos[1]])[1] != ident :
                    pao_matrix.append((up,pos[1]))
                    break
            up -= 1
        # 判断下边，条件结束是 到边界 and 已经存在棋子 and 隔一个棋子之后的后一个棋子，
        down = pos[0]+1
        while down < 10 and self.screen_cheeses_matrix[down][pos[1]] is None :
            pao_matrix.append((down,pos[1]))
            down += 1
        down = down + 1
        while down < 10 :
            if flag == 1:
                if self.screen_cheeses_matrix[down][pos[1]] is None:
                    pao_forbix.append((down,pos[1]))
                elif self.screen_cheeses_matrix[down][pos[1]] is not None:
                    pao_forbix.append((down,pos[1]))
                    break
            else:
                if self.screen_cheeses_matrix[down][pos[1]] is not None and (self.screen_cheeses_matrix[down][pos[1]])[1] != ident :
                    pao_matrix.append((down,pos[1]))
                    break
            down += 1

        if flag == 1:
            self.forbidden_zone += pao_forbix
        elif flag == 2:
            for n in pao_matrix:
                move_matrix.append((pos,n))
            self.can_move += move_matrix
        else:
            self.can_matrix += pao_matrix

    def bingzu(self,pos,ident,flag=0):
        bingzu_matrix = []
        move_matrix = []
        # 兵、卒  未过河向前走，过河之后，向左右前 只能走一格
        if ident == 1:
            # 兵
            curr_bing = [(pos[0]-1,pos[1]),(pos[0],pos[1]+1),(pos[0],pos[1]-1)]
            if pos[0] < 5:
                for i in curr_bing:
                    if flag == 1:
                        if (0 <= i[0] <= 8) and (0 <= i[1] <= 9) and (self.screen_cheeses_matrix[i[0]][i[1]] is None or (self.screen_cheeses_matrix[i[0]][i[1]])[1] == ident):
                            bingzu_matrix.append(i)
                    else:
                        if (0 <= i[0] <= 8) and (0 <= i[1] <= 9) and (self.screen_cheeses_matrix[i[0]][i[1]] is None or (self.screen_cheeses_matrix[i[0]][i[1]])[1] != ident):
                            bingzu_matrix.append(i)
            else :
                if (self.screen_cheeses_matrix[pos[0]-1][pos[1]] is None or (self.screen_cheeses_matrix[pos[0]-1][pos[1]])[1] != ident):
                    bingzu_matrix.append(curr_bing[0])
        elif ident == 2:
            # 卒
            curr_bing = [(pos[0]+1,pos[1]),(pos[0],pos[1]+1),(pos[0],pos[1]-1)]
            if pos[0] > 4:
                for i in curr_bing:
                    if flag == 1:
                        if (0 <= i[0] <= 8) and (0 <= i[1] <= 9) and (self.screen_cheeses_matrix[i[0]][i[1]] is None or (self.screen_cheeses_matrix[i[0]][i[1]])[1] == ident):
                            bingzu_matrix.append(i)
                    else:
                        if (0 <= i[0] <= 8) and (0 <= i[1] <= 9) and (self.screen_cheeses_matrix[i[0]][i[1]] is None or (self.screen_cheeses_matrix[i[0]][i[1]])[1] != ident):
                            bingzu_matrix.append(i)
            else :
                if (self.screen_cheeses_matrix[pos[0]+1][pos[1]] is None or (self.screen_cheeses_matrix[pos[0]+1][pos[1]])[1] != ident):
                    bingzu_matrix.append(curr_bing[0])

        if flag == 1:
            self.forbidden_zone += bingzu_matrix
        elif flag == 2:
            for n in bingzu_matrix:
                move_matrix.append((pos,n))
            self.can_move += move_matrix
        else:
            self.can_matrix += bingzu_matrix


    # 将帅走的时候的判断，返回对方可过河棋子的所有可供选点在将帅府九宫格内的坐标点
    # params  pos 点击的点位坐标
    # params  cheesetype  棋子的类型 chlist
    # params  ident2  黑 2 ，红 1
    def forbidden(self,ident2,flag=1):
        enemy_ident = 3-ident2
        can_jiang = [(0,3),(0,4),(0,5),(1,3),(1,4),(1,5),(2,3),(2,4),(2,5)]
        can_shuai = [(9,3),(9,4),(9,5),(8,3),(8,4),(8,5),(7,3),(7,4),(7,5)]
        enemy_list = []
        if flag == 1:
            cheese_types = (1,2,6,7,5)
        else:
            cheese_types = (1,2,3,4,6,7)
        # 获取所有对方可过河棋子的位置
        for j in range(10):
            for i in range(9):
                temp = self.screen_cheeses_matrix[j][i]

                if temp is not None and temp[1] == enemy_ident and temp[2] in cheese_types:
                    enemy_list.append((j,i))

        #print(self.screen_cheeses_matrix)
        for i in enemy_list:
            pos = i
            cheesetype = self.screen_cheeses_matrix[i[0]][i[1]][2]
            ident = enemy_ident
            jiang = [(7,9),(0,2)]

            if cheesetype == 1:
                self.ju(pos,ident,flag)
            elif cheesetype == 2:
                self.ma(pos,ident,flag)
            elif cheesetype == 5:
                can_jiang_pos = []
                # 判断将帅的竖直方向直到有棋子为止
                if ident == 1:
                    #帅的竖直方向，向上
                    up = pos[0]-1
                    while up >= 0 :
                        if self.screen_cheeses_matrix[up][pos[1]] is None:
                            can_jiang_pos.append((up,pos[1]))
                        elif self.screen_cheeses_matrix[up][pos[1]] is not None:
                            if self.screen_cheeses_matrix[up][pos[1]][2] == 5:
                                self.is_dui=1
                            break
                        up -= 1
                else:
                    #将的竖直方向，向下
                    down = pos[0]+1
                    while down < 10 :
                        if self.screen_cheeses_matrix[down][pos[1]] is None:
                            can_jiang_pos.append((down,pos[1]))
                        elif self.screen_cheeses_matrix[down][pos[1]] is not None:
                            if self.screen_cheeses_matrix[down][pos[1]][2] == 5:
                                self.is_dui=1
                            break
                        down += 1
                self.forbidden_zone += can_jiang_pos

            elif cheesetype == 6:
                self.pao(pos,ident,flag)

            elif cheesetype == 7:
                self.bingzu(pos,ident,flag)
            elif cheesetype == 3:
                self.xiang(pos,ident)
            elif cheesetype == 4:
                self.xiang(pos,ident)

        if flag == 1:
            #去掉不在将帅府九宫格的点
            forbid = []
            #print('可过河棋子的所有可行位置',self.forbidden_zone)
            for i in self.forbidden_zone:
                if (jiang[ident2-1][0] <= i[0] <= jiang[ident2-1][1]) and (3 <= i[1] <= 5):
                    forbid.append(i)

            #print("过滤掉多余的点位：",forbid)
            self.forbidden_zone = forbid;

    # 棋子走完的时候，判断是否将军
    def is_jiang(self,ident,flag=0):
        # 如果走完之后，自己的将军，就报不能走
        # 如果是对方将军，就显示将军，
        # 而且限制对方要解将
        #
        # 获取将帅的位置
        # 假设是车 看能吃到对方的車，就为将军
        # 假设是炮 能吃到对方的炮 就为将军
        # 假设是馬，能吃到对方的馬就为将军 （马脚是反方向的）
        # 假设是过河兵（卒） 能吃到对方的兵（卒） 即为将军
        # 先判断 帅
        #
        # 少一个判断绝杀
        self.forbidden_zone=[]
        pos = self.zhu_pos[0]
        self.forbidden(1)
        if pos in self.forbidden_zone:
            self.zhu[0] = 1
        else:
            self.zhu[0] = 0

        self.forbidden_zone=[]
        pos = self.zhu_pos[1]
        self.forbidden(2)
        if pos in self.forbidden_zone:
            self.zhu[1] = 1
        else:
            self.zhu[1] = 0

        if self.zhu[ident-1] == 1:
            # 己方被将
            return 1
        elif self.zhu[(3-ident)-1] == 1:
            if flag == 0 :
                res = self.is_game_over(3-ident)
            else:
                res = 2

            #对方被将
            return res
        else:
            return 3

    # 判断是否结束，即被将死了
    def is_game_over(self,ident):
        #pass
        # 获取将帅的位置
        pos = self.zhu_pos[ident-1]
        # 1 判断将还能不能走，
        self.can_matrix = []
        self.jiang(pos,ident)
        if len(self.can_matrix):
            return 2

        # 获取乙方所有棋子的所有可行位置
        self.forbidden(3-ident,2)
        # 生成所有走法
        #print(self.can_move)
        # 2 走一步，判断是否将军，是否，返回走下一步，不是，返回 0 直到所有走法完成


        result=4
        for n in self.can_move:
            pos1 = n[0]
            pos2 = n[1]
            move_cheese = self.screen_cheeses_matrix[pos1[0]][pos1[1]]
            kill_cheese = self.screen_cheeses_matrix[pos2[0]][pos2[1]]
            self.screen_cheeses_matrix[pos2[0]][pos2[1]] = kill_cheese
            self.screen_cheeses_matrix[pos1[0]][pos1[1]] = None

            res = self.is_jiang(3-ident,1)
            self.screen_cheeses_matrix[pos2[0]][pos2[1]] = kill_cheese
            self.screen_cheeses_matrix[pos1[0]][pos1[1]] = move_cheese
            if res != 2 :
                result = 2
                break


        return result


    def draw_baiqi(self,new_matrix=None):
        if new_matrix is not None:
            self.screen_cheeses_matrix = new_matrix
        else:
            cheeses_black = ['車','馬','象','士','将','炮','卒']
            cheeses_red = ['車','馬','相','仕','帅','砲','兵']

            # 定义一个棋盘的指点
            matrix = [[None]*9 for i in range(10)]
            num_one = [(cheeses_black[0],2,1,(0,0),0),(cheeses_black[1],2,2,(0,1),0),(cheeses_black[2],2,3,(0,2),0),(cheeses_black[3],2,4,(0,3),0),(cheeses_black[4],2,5,(0,4),0),(cheeses_black[3],2,4,(0,5),0),(cheeses_black[2],2,3,(0,6),0),(cheeses_black[1],2,2,(0,7),0),(cheeses_black[0],2,1,(0,8),0)]
            num_three = [None,(cheeses_black[5],2,6,(2,2),0),None,None,None,None,None,(cheeses_black[5],2,6,(2,7),0),None]
            num_four = [(cheeses_black[6],2,7,(3,0),0),None,(cheeses_black[6],2,7,(3,2),0),None,(cheeses_black[6],2,7,(3,4),0),None,(cheeses_black[6],2,7,(3,6),0),None,(cheeses_black[6],2,7,(3,8),0)]

            num_ten = [(cheeses_red[0],1,1,(9,0),0),(cheeses_red[1],1,2,(9,1),0),(cheeses_red[2],1,3,(9,2),0),(cheeses_red[3],1,4,(9,3),0),(cheeses_red[4],1,5,(9,4),0),(cheeses_red[3],1,4,(9,5),0),(cheeses_red[2],1,3,(9,6),0),(cheeses_red[1],1,2,(9,7),0),(cheeses_red[0],1,1,(9,8),0)]
            num_eight = [None,(cheeses_red[5],1,6,(7,2),0),None,None,None,None,None,(cheeses_red[5],1,6,(7,7),0),None]
            num_seven = [(cheeses_red[6],1,7,(6,0),0),None,(cheeses_red[6],1,7,(6,2),0),None,(cheeses_red[6],1,7,(6,4),0),None,(cheeses_red[6],1,7,(6,6),0),None,(cheeses_red[6],1,7,(6,8),0)]

            matrix[0] = num_one
            matrix[2] = num_three
            matrix[3] = num_four
            matrix[6] = num_seven
            matrix[7] = num_eight
            matrix[9] = num_ten
            self.screen_cheeses_matrix = matrix

            self.is_down=0 # 棋子的双方 1 红，2 黑棋
            self.down_ident=1 # 是否被点击选中，1是，0否
            self.down_pos = (0,0) # 被选中的位置
            self.down_cheese = None # 被选中的棋子
            self.can_matrix=[]
            self.forbidden_zone=[]
            self.is_over = 0

        return matrix

    def get_ident(self):
        return self.down_ident

    def get_can_matrix(self):
        return self.can_matrix

    def get_note(self):
        return self.note

    def get_over(self):
        return self.is_over
    # 获取行棋记录 后面10条
    def get_cheese_log(self):
        if len(self.cheeses_log_note) <= 10:
            return self.cheeses_log_note
        else:
            return self.cheeses_log_note[-10:]

    # 上一步
    def back_down(self):
        # 获取上一步的位置
        pos = self.cheeses_log_pos.pop()
        cheese = self.cheeses_log_cheese.pop()
        self.cheeses_log_note.pop()
        screen_cheeses_matrix[pos[0][0]][pos[0][1]] = cheese[0]
        screen_cheeses_matrix[pos[1][0]][pos[1][1]] = cheese[1]




# 画出棋盘
# param surf 画布
def draw_background(surf):
    # 加载背景图片
    surf.blit(background_img,(0,0))

    # 画网格线，棋盘为 19X19
    # 1 画出边框，这里 grid_width = width // 20
    # draw.line (画布，颜色，始点坐标，终点坐标，宽度=1)
    #  左上 (72,72)  左下 (72,792-72)  右上 (720-72,72) 右下 (720-72,792-72)
    # [
    #   ((72,72),(72,792-72))   左边界
    #   ((72,72),(720-72,72))   上边界
    #   ((72,792-72),(720-72,792-72))   下边界
    #   ((720-72,72),(720-72,792-72))   右边界
    # ]
    # 定义四个边框顶点坐标
    rect_lines = [
        ((grid_width,grid_width),(grid_width,height-grid_width)),
        ((grid_width,grid_width),(width-grid_width,grid_width)),
        ((grid_width,height-grid_width),(width-grid_width,height-grid_width)),
        ((width-grid_width,grid_width),(width-grid_width,height-grid_width)),

        ((grid_width-5,grid_width-5),(grid_width-5,height-grid_width+5)),
        ((grid_width-5,grid_width-5),(width-grid_width+5,grid_width-5)),
        ((grid_width-5,height-grid_width+5),(width-grid_width+5,height-grid_width+5)),
        ((width-grid_width+5,grid_width-5),(width-grid_width+5,height-grid_width+5)),

    ]

    for line in rect_lines:
        pygame.draw.line(surf,black,line[0],line[1],2)

    # 画出中间的网格线
    for i in range(7):
        # 画竖线
        pygame.draw.line(surf,black,(grid_width*(2+i),grid_width),(grid_width*(2+i),grid_width*5))
        pygame.draw.line(surf,black,(grid_width*(2+i),grid_width*6),(grid_width*(2+i),height-grid_width))

    # 间隔线
    pygame.draw.line(surf,black,(grid_width*10+side_width,0),(grid_width*10+side_width,height))

    for i in range(8):
        # 画横线
        pygame.draw.line(surf,black,(grid_width,grid_width*(2+i)),(width-grid_width,grid_width*(2+i)))

    # 画将府的斜线
    pygame.draw.line(surf,black,(4*grid_width,grid_width),(6*grid_width,3*grid_width))
    pygame.draw.line(surf,black,(4*grid_width,3*grid_width),(6*grid_width,grid_width))

    # 画帅府的斜线
    pygame.draw.line(surf,black,(4*grid_width,height-grid_width),(6*grid_width,height-(3*grid_width)))
    pygame.draw.line(surf,black,(4*grid_width,height-3*grid_width),(6*grid_width,height-grid_width))

    #画炮兵卒位
    # lines (画布，颜色，closed=False,pointlist,width=1)   closed 是否要闭合，True 闭合
    #  pointlist [(),(),()]
    pointlist = [(2,3),(8,3),(2,8),(8,8),(3,4),(5,4),(7,4),(3,7),(5,7),(7,7),(1,4),(1,7),(9,4),(9,7)]
    pwidth=2
    n = 1
    for j in pointlist:
        if n not in (11,12):
            # 2
            pygame.draw.lines(surf,black,False,[(grid_width*j[0]-3,grid_width*j[1]-10),(grid_width*j[0]-3,grid_width*j[1]-3),(grid_width*j[0]-10,grid_width*j[1]-3)],pwidth)
            # 3
            pygame.draw.lines(surf,black,False,[(grid_width*j[0]-3,grid_width*j[1]+10),(grid_width*j[0]-3,grid_width*j[1]+3),(grid_width*j[0]-10,grid_width*j[1]+3)],pwidth)
        if n not in (13,14):
            # 1
            pygame.draw.lines(surf,black,False,[(grid_width*j[0]+3,grid_width*j[1]-10),(grid_width*j[0]+3,grid_width*j[1]-3),(grid_width*j[0]+10,grid_width*j[1]-3)],pwidth)
            # 4
            pygame.draw.lines(surf,black,False,[(grid_width*j[0]+3,grid_width*j[1]+10),(grid_width*j[0]+3,grid_width*j[1]+3),(grid_width*j[0]+10,grid_width*j[1]+3)],pwidth)
        n +=1


# 当用户点下鼠标那一刻，第一个调用的方法，即为入口
# surf  画布
# pos 用户落子的位置
def move(pos):
    # 获取鼠标点击坐标值，然后进行除于 grid_width 四舍五入取整 获取坐标点
    grid = (int(round(pos[1]/(grid_width + .0)))-1,int(round(pos[0]/(grid_width + .0))-1))
    #print(grid)
    # 判断是否点到了边界
    if grid[0] < 0 or grid[0] > 9:
        return False
    if grid[1] < 0 or grid[1] > 8:
        return False
    # 重新赋值 pos
    ##pos = (grid[0] * grid_width,grid[1]*grid_width)
    return grid


def show_go_screen(surf,winner=0):
    note_height = 10
    if winner == 1:
        draw_txt(surf,'你 {0} ！'.format('赢 了' if winner == USER else '输 了'),(width//2,note_height),64,0,red)
    else:
        screen.blit(background,back_rect)
    draw_txt(surf,"中国象棋",(width//2,note_height+height//4),64,0,black)
    draw_txt(surf,"请按任意键开始",(width//2,note_height+height//2),22,0,blue)
    pygame.display.flip()
    waiting = True

    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = 0
running = True
clock = pygame.time.Clock()
fps=30
m = 0
ident=1
# 初始化棋盘
cheese = cheese()
curr_cheess_matrix = None
screen_cheeses_matrix = cheese.draw_baiqi(curr_cheess_matrix)
can_matrix = []
cheese_log = [None]*10
note=""
game_over = True
winner = 0
while running:
    if game_over:
        show_go_screen(screen, winner)
        game_over = False
        screen_cheeses_matrix=cheese.draw_baiqi()

    # 设置屏幕刷新频率
    clock.tick(fps)
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            curr_pos = move(event.pos)
            if curr_pos:
                screen_cheeses_matrix = cheese.power_down(curr_pos,ident)
                can_matrix = cheese.get_can_matrix()
                ident = cheese.get_ident()
                note = cheese.get_note()
                cheese_log = cheese.get_cheese_log()
                winner = cheese.get_over()
                #cheese_log.reverse()

    draw_background(screen)
    writeTxt(screen)
    # 画棋子
    for j in range(10):
        for i in range(9):
            temp = screen_cheeses_matrix[j][i]
            if temp is not None:
                if temp[1] == 1:
                    curr_color = cheese_color_red
                elif temp[1] == 2:
                    curr_color = cheese_color_black
                elif temp[1] == 3:
                    curr_color = cheese_color_blue
                draw_cheese(screen,curr_color,((i+1)*grid_width,(j+1)*grid_width),temp[0])
    # 画可行点
    for z in can_matrix:
        pygame.draw.circle(screen,blue,((z[1]+1)*grid_width,(z[0]+1)*grid_width),8)

    if note != '':
        draw_txt(screen,note,(width/2-40,height/2-40),66,0,red)

    # 显示记录
    lenstr = len(cheese_log)
    for n in range(lenstr):
        if cheese_log[n]:
            draw_txt(screen,cheese_log[n],(grid_width*11+side_width,(grid_width-30)*n+30),25,0,white)

    if winner == 1:
        game_over=True

    if m > 10000:
        running = False
    m += 1
    #print(m)
    # 刷新屏幕
    pygame.display.flip()
