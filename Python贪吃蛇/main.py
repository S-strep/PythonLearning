import pygame
import codecs
import pygame.font
import math  # 调用数学库函数
from pygame.locals import *
from sys import exit
from settings import Settings
import random


class Point():
    row = 0
    clo = 0

    def __init__(self, row, clo):
        self.row = row
        self.clo = clo

    def copy(self):
        return Point(row=self.row, clo=self.clo)

ai_settings = Settings()
# 蛇头坐标定在中间
head = Point(row=int(ai_settings.row / 2), clo=int(ai_settings.clo / 2))
window = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
# 初始化蛇身的元素数量
snake = [
        Point(row=head.row, clo=head.clo + 1),
        Point(row=head.row, clo=head.clo + 2),
        Point(row=head.row, clo=head.clo + 3)
    ]



def main():
    # 初始化
    pygame.init()
    pygame.mixer.init()  #初始化
    font_list = pygame.font.get_fonts()  # 获取所有可使用的字体
    font1 = pygame.font.SysFont('./font/myfont.ttf', 16, True)    # 创建一个Font对象，字体为默认并且圆滑。
    font2 = pygame.font.SysFont('None', 16, True)  # 创建Font对象
    direct = 'left'
    food_score = 100      # 单一食物的得分
    top_score = 0      # 最高分
    score = 0           # 得分
    num = 0             # 已吃得的食物数量
    filename='scores.txt'    # 储存得分的文件
    grade = 1  # 当前等级
    bonus = 200  # 过一关的额外奖励
    pygame.display.set_caption('贪吃蛇')
    game_font = pygame.font.SysFont('./font/myfont.ttf', 25, True)   # 创建另一个Font对象
    head = Point(row=int(ai_settings.row / 2), clo=int(ai_settings.clo / 2))
    snake = [
        Point(row=head.row, clo=head.clo + 1),
        Point(row=head.row, clo=head.clo + 2),
        Point(row=head.row, clo=head.clo + 3)
    ]



    ck = pygame.display.set_mode((800,400))   #  游戏窗口
    start_ck = pygame.Surface(ck.get_size())    #   充当开始界面的画布
    start_ck = start_ck.convert()
    start_ck.fill((255,255,255))  # 白色画布1（开始界面用的）
    # 加载各个素材图片 并且赋予变量名
    i1 = pygame.image.load("./images/s1.png")
    i1.convert()
    i11 = pygame.image.load("./images/s2.png")
    i11.convert()

    i2 = pygame.image.load("./images/n2.png")
    i2.convert()
    i21 = pygame.image.load("./images/n1.png")
    i21.convert()
    pygame.mixer.music.load("bgm.mp3")  # 加载音乐文件


    #  以下为选择开始界面鼠标检测结构。

    n1 = True
    while n1:

        pygame.mixer.music.play()  #播放音乐
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        if x1 >= 227 and x1 <= 555 and y1 >= 91 and y1 <=167:
            start_ck.blit(i11, (200, 70))
            if buttons[0]:
                n1 = False

        elif x1 >= 227 and x1 <= 555 and y1 >= 211 and y1 <=277:
            start_ck.blit(i21, (200, 190))
            if buttons[0]:
                pygame.quit()
                exit()

        else:
            start_ck.blit(i1, (200, 80))
            start_ck.blit(i2, (200, 200))


        ck.blit(start_ck,(0,0))
        pygame.display.update()

        # 下面是监听退出动作

        # 监听事件
        for event in pygame.event.get():

            # 判断事件类型是否是退出事件
            if event.type == pygame.QUIT:
                print("游戏退出...")

                # quit 卸载所有的模块
                pygame.quit()

                # exit() 直接终止当前正在执行的程序
                exit()


    # 定义坐标

    # 食物坐标
    snakeFood = gen_food()

    quit = True
    # 设置帧频率
    clock = pygame.time.Clock()
    while quit:
        time = ai_settings.tick_time+grade*5  #设置可变循环频率
        # 处理帧频
        clock.tick(time)
        # pygame.event.get()获取当前事件的队列 可以同时发生很多事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = False
            elif event.type == pygame.KEYDOWN:
                # 这里小细节蛇不可以直接左右上下 要判断当前是在什么状态下前行
                if event.key == 273 or event.key == 119:
                    if direct == 'left' or direct == 'right':
                        direct = 'top'
                if event.key == 274 or event.key == 115:
                    if direct == 'left' or direct == 'right':
                        direct = 'bottom'
                if event.key == 276 or event.key == 97:
                    if direct == 'top' or direct == 'bottom':
                        direct = 'left'
                if event.key == 275 or event.key == 100:
                    if direct == 'top' or direct == 'bottom':
                        direct = 'right'
        # 吃东西
        eat = (head.row == snakeFood.row and head.clo == snakeFood.clo)

        # 处理蛇的身子
        # 1.把原来的头插入到snake的头上
        # 2.把最后一个snake删掉
        if eat:
            snakeFood = Point(row=random.randint(0, ai_settings.row - 1), clo=random.randint(0, ai_settings.clo - 1))
            num = num + 1
            if (num - 3) % 3 == 0:  # 判断已过关
                score = score + bonus
            else:
                score = score + 100
            grade = math.ceil(num / 3)
        snake.insert(0, head.copy())
        if not eat:
            snake.pop()

        with open(filename, 'a') as file_object:
            file_object.write(str(score) + "\n")    # 写入当前得分


        with open(filename) as file_object1:
            lines = file_object1.readlines()      # 按行读取历史得分

        for line in lines:
            if int(line.rstrip()) > top_score:
                top_score = int(line.rstrip())      # 转化为int型后与此前的最高分比较，以更新最高分

        # 移动一下
        if direct == 'left':
            head.clo -= 1
        if direct == 'right':
            head.clo += 1
        if direct == 'top':
            head.row -= 1
        if direct == 'bottom':
            head.row += 1
        dead = False
        if head.clo < 0 or head.row < 0 or head.clo >= ai_settings.clo or head.row >= ai_settings.row:
            dead = True
        for body in snake:
            if head.clo == body.clo and head.row == body.row:
                dead = True
                break
        if dead:
            print('Game Over')
            show_gameover_info(window)
        # 背景画图
        pygame.draw.rect(window, ai_settings.bg_color, (0, 0, ai_settings.screen_width, ai_settings.screen_height))

        # 蛇头
        rect(head, ai_settings.head_color)
        # 绘制食物
        rect(snakeFood, ai_settings.snakeFood_color)
        # 绘制蛇的身子
        for body in snake:
            rect(body, ai_settings.body_color)

        window.blit(game_font.render('scores: %d' % score, True, [0, 0, 0]), [650, 10])  # 在屏幕中间打印当前得分
        window.blit(game_font.render('top scores: %d' % top_score, True, [255, 0, 0]), [325, 10])   #在屏幕右上角打印最高分
        window.blit(game_font.render('garde: %d' % grade, True, [255, 255, 0]), [25, 10])  # 在屏幕左上角打印当前等级
        # 交还控制权
        pygame.display.flip()

def show_gameover_info(window):
    font = pygame.font.Font('./font/myfont.ttf', 32)
    tip = font.render('  按Q或者ESC退出游戏, 按R键重新开始游戏', True,  (65, 105, 225))
    gamestart = pygame.image.load('./images/gameover.png')
    window.blit(gamestart, (0, 0))
    window.blit(tip, (80, 300))
    pygame.display.update()

    while True:  #键盘监听事件
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                exit()     #终止程序
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:  #终止程序
                    exit()  #终止程序
                elif event.key == K_r:

                    main()  #结束此函数, 重新开始游戏


# 生成食物并且不让食物生成在蛇的身体里面
def gen_food():
    while 1:
        position = Point(row=random.randint(0, ai_settings.row - 1), clo=random.randint(0, ai_settings.clo - 1))
        is_coll = False
        if head.row == position.row and head.clo == position.clo:
            is_coll = True
        for body in snake:
            if body.row == position.row and body.clo == position.clo:
                is_coll = True
                break
        if not is_coll:
            break
    return position


# 需要执行很多步画图操作 所以定义一个函数
def rect(point, color):
    # 定位 画图需要left和top
    left = point.clo * ai_settings.screen_width / ai_settings.clo
    top = point.row * ai_settings.screen_height / ai_settings.row
    # 将方块涂色
    pygame.draw.rect(window, color, (left, top, ai_settings.screen_width / ai_settings.clo, ai_settings.screen_height / ai_settings.row))

main()