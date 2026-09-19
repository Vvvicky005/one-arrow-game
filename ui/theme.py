"""
配色、字体、布局、参数。
"""

import pygame

WIDTH = 900
HEIGHT = 700
FPS = 60

# 颜色
WHITE = (255, 255, 255)
BLACK = (45, 55, 75)
BG_TOP = (220, 242, 255)
BG_BOTTOM = (245, 250, 255)
BLUE = (96, 165, 250)
DARK_BLUE = (59, 130, 246)
PINK = (244, 114, 182)
LIGHT_PINK = (252, 165, 205)
PURPLE = (167, 139, 250)
GREEN = (74, 222, 128)
RED = (248, 113, 113)
YELLOW = (250, 204, 21)
ORANGE = (251, 146, 60)
CELL_BG = (255, 255, 255)
CELL_BORDER = (214, 226, 240)

ARROW_COLORS = [
    (96, 165, 250),
    (244, 114, 182),
    (167, 139, 250),
    (74, 222, 128),
    (251, 146, 60),
    (45, 190, 190),
]

# 棋盘
ROWS = 6
COLS = 6
CELL_SIZE = 72
BOARD_X = 215
BOARD_Y = 145

# 规则参数
MAX_MISTAKES = 3
CORRECT_SCORE = 100
MISTAKE_SCORE = 50
HINT_SCORE = 100

_font_cache = {}

def get_font(size):
    if size not in _font_cache:
        try:
            _font_cache[size] = pygame.font.Font("C:/Windows/Fonts/msyh.ttc", size)
        except Exception:
            _font_cache[size] = pygame.font.SysFont("microsoftyahei", size)
    return _font_cache[size]