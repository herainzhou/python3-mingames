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

black=(0,0,0)
red=(251,4,4)

cheese_color_red = (251,4,5)
cheese_color_black = (10,10,10)



# 加载背景图片
base_folder = os.path.dirname(__file__)
img_folder = os.path.join(base_folder,'images')
background_img=pygame.image.load(os.path.join(img_folder,'back.png'))





screen = pygame.display.set_mode((width+side_width, height))
pygame.display.set_caption("中国象棋")

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


def draw_baiqi():


    cheeses_black = ['車','馬','象','士','将','炮','卒']
    cheeses_red = ['車','馬','相','仕','帅','炮','兵']

    # 定义一个棋盘的指点
    screen_cheeses_matrix = [[None]*9 for i in range(10)]
    num_one = [(cheeses_black[0],2),(cheeses_black[1],2),(cheeses_black[2],2),(cheeses_black[3],2),(cheeses_black[4],2),(cheeses_black[3],2),(cheeses_black[2],2),(cheeses_black[1],2),(cheeses_black[0],2)]
    num_three = [None,(cheeses_black[5],2),None,None,None,None,None,(cheeses_black[5],2),None]
    num_four = [(cheeses_black[6],2),None,(cheeses_black[6],2),None,(cheeses_black[6],2),None,(cheeses_black[6],2),None,(cheeses_black[6],2)]

    num_ten = [(cheeses_red[0],1),(cheeses_red[1],1),(cheeses_red[2],1),(cheeses_red[3],1),(cheeses_red[4],1),(cheeses_red[3],1),(cheeses_red[2],1),(cheeses_red[1],1),(cheeses_red[0],1)]
    num_eight = [None,(cheeses_red[5],1),None,None,None,None,None,(cheeses_red[5],1),None]
    num_seven = [(cheeses_red[6],1),None,(cheeses_red[6],1),None,(cheeses_red[6],1),None,(cheeses_red[6],1),None,(cheeses_red[6],1)]

    screen_cheeses_matrix[0] = num_one
    screen_cheeses_matrix[2] = num_three
    screen_cheeses_matrix[3] = num_four
    screen_cheeses_matrix[6] = num_seven
    screen_cheeses_matrix[7] = num_eight
    screen_cheeses_matrix[9] = num_ten
    return screen_cheeses_matrix


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


running = True
clock = pygame.time.Clock()
fps=30
j = 0
# 初始化棋盘
screen_cheeses_matrix = draw_baiqi()

while running:
    # 设置屏幕刷新频率
    clock.tick(fps)
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    draw_background(screen)
    writeTxt(screen)
    # 画棋子
    #

    for j in range(10):
        for i in range(9):
            temp = screen_cheeses_matrix[j][i]
            if temp is not None:
                draw_cheese(screen,(cheese_color_red if temp[1] == 1 else cheese_color_black),((i+1)*grid_width,(j+1)*grid_width),temp[0])

    # 刷新屏幕
    if j > 100:
        running = False
    j += 1
    pygame.display.flip()
