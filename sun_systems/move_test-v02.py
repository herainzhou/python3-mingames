# -*- coding: utf-8 -*-
# 导入我们需要用到的包
import pygame
import os
import math,time



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
width = 72*14
height = 72*14
grid_width = width // 12
# 中点
center_pos = (int(width/2),int(height/2))
print(center_pos)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("太阳系")

white = (255,255,255)

sun = ('#ff0','#f90')
sun = ((255,255,0),(255,153,0))

# 太阳，水，金，地，火，木，土，天，海

beginColor              = ("#A69697", "#C4BBAC", "#78B1E8", "#CEC9B6", "#C0A48E", "#F7F9E3", "#A7E1E5", "#0661B2")
beginColor              = ((166,150,151), (196,187,172), (120,177,232), (206,201,182), (192,164,142), (247,249,227), (167,225,229), (6,97,178))
endColor                = ("#5C3E40", "#1F1315", "#050C12", "#76422D", "#322222", "#5C4533", "#19243A", "#1E3B73")
cycle                   = (87.70, 224.701, 365.2422, 686.98, 4332.589, 10759.5, 30799.095, 60152)
#cycle                   = (87.70, 224.701, 365.2422, 686.98, 4332.589, 706.98, 301, 400)
sun_radius_rate         = (0.387, 0.723, 1, 1.523, 5.202, 9.554, 19, 30.106)
sun_radius_rate         = (0.387, 0.723, 1, 1.5, 2, 3, 4, 4.5)
local_radius_rate       = (0.5, 1, 1, 0.7, 3, 2.5, 2.3, 2)


line_marix = []
# 画出棋盘
# param surf 画布
def draw_background(surf,num=0):
    # 加载背景图片
    surf.blit(background_img,(0,0))

    # 中点位置画太阳
    pygame.draw.circle(surf,sun[0],center_pos,25)

    lenght = len(sun_radius_rate)
    for i in sun_radius_rate:
        pygame.draw.circle(surf,white,center_pos,int(i*100),1)
    lines = []
    for j in range(lenght):
        w = int(cycle[j])
        z = num%w
        pos = draw_planet(sun_radius_rate[j],z,w)
        pygame.draw.circle(surf,beginColor[j],pos,int(local_radius_rate[j]*10))
        #if j == 6 or j == 7:
        #    lines.append(pos)
    line_marix.append(lines)

    for n in line_marix:
        pass
        #pygame.draw.line(surf,white,n[0],n[1])


def wrap_angle(angle):
    return abs(angle % 360)

# 算圆上的点坐标
def draw_planet(radius=1,num=0,w=0):
    radius = radius*100
    dot = center_pos
    planet_angle = wrap_angle(num * (360/w)-90)
    planet_angle = math.radians(planet_angle)
    min_x = math.cos(planet_angle)*(radius)
    min_y = math.sin(planet_angle)*(radius)
    target = (int(dot[0]+min_x),int(dot[1]+min_y))
    return target


#draw_planet()


running = True
clock = pygame.time.Clock()
fps=100
num=0

while running:
    # 设置屏幕刷新频率
    clock.tick(fps)
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_background(screen,num)
    # 刷新屏幕
    pygame.display.flip()
    num +=20
