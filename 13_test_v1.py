# -*- coding: utf-8 -*-
# 导入我们需要用到的包
import pygame
import os


'''
一划三，开发思路 流程
1：先画网格
2：走子，判断
3：判断胜负

游戏规则：
1：摆棋。黑子、白子互相对立 （一人一步）
2：走法规则，只能走一格而且为空格，已经有子了不能走，出界也不能走
3：走一步判断横竖是否有一划三 或者 三划一
4：如果3有是换子
5：直到只剩下一种颜色的棋子为止
6：点击蓝色的棋子为取消选中

'''

# 初始化
pygame.init()

# 初始化 mixer (导入背景音乐)
pygame.mixer.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

# 加载背景图片
base_folder = os.path.dirname(__file__)
img_folder = os.path.join(base_folder,'images')
background_img = pygame.image.load(os.path.join(img_folder,'back.png'))

# 设置宽高
width = 216
height = 216
grid_width = width // 5
radius = 15 # 棋子半径
side_width=100
font_name = 'SimHei'


screen = pygame.display.set_mode((width+side_width, height))
pygame.display.set_caption("一划三")




class game13():
    down_ident = 0 # 棋子的双方 0 白棋，1 黑棋
    is_down = 0 # 是否被点击选中，1是，0否
    down_pos = (0,0) # 别选中的位置
    down_color = black # 被选中的颜色
    is_draction = 0 # 判断走子发方向，方便判断结果 0 横向 1 竖向

    def __init__(self):
        pass

    def create_qizi(self):
        self.down_ident=0
        self.is_down=0
        self.down_pos=(0,0)
        self.down_color=black
        self.is_draction=0
        # 生成棋盘列表 定义开始棋子位子
        #color_metrix = [[None] * 4 for i in range(4)]
        color_metrix = []
        color_metrix.append([black,black,black,black])
        color_metrix.append([None,black,None,black])
        color_metrix.append([white,None,white,None])
        color_metrix.append([white,white,white,white])
        return color_metrix

    # 鼠标按下进入方法
    # color_metrix 棋子列表
    # pos 当前鼠标按下的位置
    # curr_ident 当前下子的标识
    def power_down(self,color_metrix,pos,curr_ident=0):
        if self.is_down == 0:
            # 未选中,判断是否有棋子在，没有棋子不做为，有就显示被选中状态 一人一步
            if self.down_ident == curr_ident and color_metrix[pos[1]][pos[0]] is not None and color_metrix[pos[1]][pos[0]] != self.down_color:
                self.is_down = 1
                self.down_pos = pos
                self.down_color = color_metrix[pos[1]][pos[0]]
                color_metrix[pos[1]][pos[0]] = blue
        else:
            # 有被选中的棋子了，判断当走子与被选中的是否相差一格，而且没有棋子在当前位置上
            if color_metrix[pos[1]][pos[0]] is None:
                if pos[0] == self.down_pos[0]:
                    if pos[1]-self.down_pos[1] == 1 or pos[1]-self.down_pos[1] == -1:
                        color_metrix[pos[1]][pos[0]] = self.down_color
                        color_metrix[self.down_pos[1]][self.down_pos[0]] = None
                        self.is_down=0
                        self.down_pos=(0,0)
                        self.down_ident = 0 if self.down_ident==1 else 1
                        self.is_draction=1
                elif pos[1] == self.down_pos[1]:
                    if pos[0]-self.down_pos[0] == 1 or pos[0]-self.down_pos[0] == -1:
                        color_metrix[pos[1]][pos[0]] = self.down_color
                        color_metrix[self.down_pos[1]][self.down_pos[0]] = None
                        self.is_down=0
                        self.down_pos=(0,0)
                        self.down_ident = 0 if self.down_ident==1 else 1
                        self.is_draction=2
            elif color_metrix[pos[1]][pos[0]] == blue:
                self.is_down=0
                self.down_pos=(0,0)
                color_metrix[pos[1]][pos[0]] = self.down_color
                self.down_color = black if self.down_color == white else white
                return color_metrix

        color_metrix = self.transform_qizi(pos,color_metrix)

        return color_metrix

    #
    def transform_qizi(self,pos,color_metrix,direction=0):
        color_num1 = 1
        color_num2 = 0
        color_num3 = 0
        color_now = 0
        if direction == 0:
            direction = self.is_draction

        # 判断竖直方向
        if direction == 1:
            # 只判断横向就行了
            # 如果有3个同颜色的相连并且还是都有棋子的情况下，另一个在边，就要给换颜色
            # 判断3划1
            right = pos[0]+1
            while right < 4 and color_metrix[pos[1]][right] is not None and color_metrix[pos[1]][right] == self.down_color:
                color_num1 += 1
                right += 1

            left = pos[0]-1
            while left >= 0 and color_metrix[pos[1]][left] is not None and color_metrix[pos[1]][left] == self.down_color:
                color_num1 += 1
                left -= 1

            # 判断 1划3
            if pos[0]+1 >= 4:
                # 看左边三个
                left = pos[0]-1
                color_now = color_metrix[pos[1]][left]
                while left >= 0 and color_metrix[pos[1]][left] is not None and color_metrix[pos[1]][left] == color_now:
                    color_num2 += 1
                    left -= 1
            if pos[0]-1 < 0 :
                # 看右边三个
                right = pos[0]+1
                color_now = color_metrix[pos[1]][right]
                while right < 4 and color_metrix[pos[1]][right] is not None and color_metrix[pos[1]][right] == color_now:
                    color_num3 += 1
                    right += 1
            if color_num1 == 3 or color_num2 == 3 or color_num3 == 3:
                # 换颜色
                for i in range(4):
                    if color_metrix[pos[1]][i] is not None and color_metrix[pos[1]][i] != self.down_color:
                        color_metrix[pos[1]][i] = self.down_color
                        pos_son = (i,pos[1])
                        color_metrix = self.transform_qizi(pos_son,color_metrix,2)

        elif direction == 2:
            # 只判断竖向就行了
            # 如果有3个同颜色的相连，另一个在边，就要给换颜色
            # 判断3划1
            down = pos[1]+1
            while down < 4 and color_metrix[down][pos[0]] is not None and color_metrix[down][pos[0]] == self.down_color:
                color_num1 += 1
                down += 1

            up = pos[1]-1
            while up >= 0 and color_metrix[up][pos[0]] is not None and color_metrix[up][pos[0]] == self.down_color:
                color_num1 += 1
                up -= 1

            # 判断 1划3
            if pos[1]+1 >= 4:
                # 看上边三个
                up = pos[1]-1
                color_now = color_metrix[up][pos[0]]
                while up >= 0 and color_metrix[up][pos[0]] is not None and color_metrix[up][pos[0]] == color_now:
                    color_num2 += 1
                    up -= 1
            if pos[1]-1 < 0 :
                # 看下边三个
                down = pos[1]+1
                color_now = color_metrix[down][pos[0]]
                while down < 4 and color_metrix[down][pos[0]] is not None and color_metrix[down][pos[0]] == color_now:
                    color_num3 += 1
                    down += 1
            if color_num1 == 3 or color_num2 == 3 or color_num3 == 3:
                # 换颜色
                for i in range(4):
                    if color_metrix[i][pos[0]] is not None and color_metrix[i][pos[0]] != self.down_color:
                        color_metrix[i][pos[0]] = self.down_color
                        pos_son = (pos[0],i)
                        color_metrix = self.transform_qizi(pos_son,color_metrix,1)

        return color_metrix


    def get_ident(self):
        return self.down_ident

    def get_color(self):
        return self.down_color

    def set_down_color(self,color):
        self.down_color = color
        return self.down_color








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
        pygame.draw.line(surf,black,line[0],line[1],1)

    # 画出中间的网格线
    for i in range(3):
        # 画竖线
        pygame.draw.line(surf,black,(grid_width*(2+i),grid_width),(grid_width*(2+i),height-grid_width))
        # 画横线
        pygame.draw.line(surf,black,(grid_width,grid_width*(2+i)),(height-grid_width,grid_width*(2+i)))


# 画棋子
def draw_qizi(surf,color_metrix=None):
    if color_metrix is not None:
        for i in range(4):
            for j in range(4):
                if color_metrix[i][j] is not None:
                    pygame.draw.circle(surf,color_metrix[i][j],((j+1)*grid_width,(i+1)*grid_width),radius)

# 画文字模块
# surf  画布
# text  文字
# size  字体大小
# pos   显示方位 （0,0）
# color 显示颜色值
def draw_text(surf,text,size,pos,color=white):
    text_surface = pygame.font.SysFont(font_name,size).render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = pos
    surf.blit(text_surface,text_rect)

# 判断胜负
# 当棋盘里所有的棋子都是同一种颜色就表示已经结束了
def game_is_over(color_metrix):
    b = 0
    w = 0
    for i in range(4):
        for j in range(4):
            if color_metrix[i][j] is not None and color_metrix[i][j] == black:
                b += 1
            if color_metrix[i][j] is not None and color_metrix[i][j] == white:
                w += 1

    if b == 12 :
        return 2
    elif w == 12:
        return 1
    return 0

# 显示输赢
def show_go_screen(surf,winner=None):
    note_height = 10
    if winner is not None:
        draw_text(surf,' {0} 赢 了！'.format('白棋' if winner == 0 else '黑棋'),14,(width//2,note_height),red)
    else:
        screen.blit(background_img,(0,0))
    draw_text(surf,"一划三",14,(width//2,note_height+height//4),black)
    draw_text(surf,"请按任意键开始",12,(width//2,note_height+height//2),blue)
    pygame.display.flip()
    waiting = True

    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False


# 当用户点下鼠标那一刻，第一个调用的方法，即为入口
# surf  画布
# pos 用户落子的位置
def move(pos):
    # 获取鼠标点击坐标值，然后进行除于 grid_width 四舍五入取整 获取坐标点
    grid = (int(round(pos[0]/(grid_width + .0))-1),int(round(pos[1]/(grid_width + .0)))-1)
    #print(grid)
    # 判断是否点到了边界
    if grid[0] < 0 or grid[0] > 4:
        return
    if grid[1] < 0 or grid[1] > 4:
        return
    # 重新赋值 pos
    pos = (grid[0] * grid_width,grid[1]*grid_width)

    return grid


running = True
game_over = True
winner = None
clock = pygame.time.Clock()
fps=30
ident = 0
win = 0
gm13 = game13()

color = (white,black)
while running:
    if game_over:
        # 显示输赢信息
        show_go_screen(screen,winner)
        # 游戏结束，重新初始化
        game_over = False
        color_metrix = gm13.create_qizi()

    # 设置屏幕刷新频率
    clock.tick(fps)
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            curr_pos = move(event.pos)
            color_metrix = gm13.power_down(color_metrix,curr_pos,ident)
            ident = gm13.get_ident()
    draw_background(screen)
    draw_qizi(screen,color_metrix)
    # 判断胜负
    win = game_is_over(color_metrix)
    if win > 0:
        winner=win-1
        game_over = True
    if win == 0:
        draw_text(screen,"轮到{0} ".format('白棋' if ident == 0 else '黑棋'),24,(width+50,height//2),color[ident])
    else:
        draw_text(screen,"结束了",24,(width+50,height//2),color[ident])
    # 刷新屏幕
    pygame.display.flip()
