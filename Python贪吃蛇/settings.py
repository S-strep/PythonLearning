class Settings():
    # 存储本游戏中所有设置的类
    def __init__(self):
        # 初始化游戏的设置
        # 屏幕设置
        self.screen_width = 800
        self.screen_height = 400
        self.bg_color = (0, 245, 255)
        self.row = 30
        self.clo = 40
        self.head_color = (255, 215, 0)
        self.body_color = (255, 106, 106)
        self.snakeFood_color = (255, 0, 0)
        self.snakeFoodBonus_color = (255, 0, 0)
        self.tick_time = 5
        self.score= 0
        self.num = 0
        self.filename='scores.txt'
        self.top_score= 0
        self.food_score= 0
        
