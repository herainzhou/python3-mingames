# -*- coding: utf-8 -*-
# 导入我们需要用到的包
import pygame
import os


'''
五子棋，开发思路 流程
1：先画网格
2：获取鼠标点击落子
3：判断胜负

游戏规则：
1：摆棋。黑子、白子互相对立
2：走法规则，只能走一格而且为空格，已经有子了不能走，出界也不能走
3：走一步判断横竖是否有一划三 或者 三划一
4：如果3有是换子
5：直到只剩下一种颜色的棋子为止
'''

# 初始化
pygame.init()

# 初始化 mixer (导入背景音乐)
pygame.mixer.init()

black = (0,0,0)

# 加载背景图片
base_folder = os.path.dirname(__file__)
img_folder = os.path.join(base_folder,'images')
background_img = pygame.image.load(os.path.join(img_folder,'back.png'))

# 设置宽高
width = 216
height = 216
grid_width = width // 5


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("一划三")



# 画出棋盘
# param surf 画布
def draw_background(surf):
    # 加载背景图片
    surf.blit(background_img,(0,0))

    # 画网格线，棋盘为 19X19
    # 1 画出边框，这里 grid_width = width // 20
    # draw.line (画布，颜色，始点坐标，终点坐标，宽度=1)
    # 定义四个边框顶点坐标
    rect_lines = [
        ((grid_width,grid_width),(grid_width,height-grid_width)),
        ((grid_width,grid_width),(width-grid_width,grid_width)),
        ((grid_width,height-grid_width),(width-grid_width,height-grid_width)),
        ((width-grid_width,grid_width),(width-grid_width,height-grid_width)),
    ]

    for line in rect_lines:
        pygame.draw.line(surf,black,line[0],line[1],2)

    # 画出中间的网格线
    for i in range(17):
        # 画竖线
        pygame.draw.line(surf,black,(grid_width*(2+i),grid_width),(grid_width*(2+i),height-grid_width))
        # 画横线
        pygame.draw.line(surf,black,(grid_width,grid_width*(2+i)),(height-grid_width,grid_width*(2+i)))


running = True
clock = pygame.time.Clock()
fps=30

while running:
    # 设置屏幕刷新频率
    clock.tick(fps)
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_background(screen)
    # 刷新屏幕
    pygame.display.flip()
