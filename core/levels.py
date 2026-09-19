"""
关卡数据。
"""

LEVELS = [
    # 第 1 关
    [
        {"row": 0, "col": 0, "direction": "up"},
        {"row": 1, "col": 2, "direction": "up"},
        {"row": 2, "col": 2, "direction": "left"},
        {"row": 3, "col": 2, "direction": "down"},
        {"row": 4, "col": 4, "direction": "right"},
        {"row": 4, "col": 3, "direction": "right"},
        {"row": 5, "col": 5, "direction": "down"},
    ],

    # 第 2 关
    [
        {"row": 0, "col": 1, "direction": "up"},
        {"row": 1, "col": 1, "direction": "down"},
        {"row": 2, "col": 1, "direction": "left"},
        {"row": 2, "col": 3, "direction": "right"},
        {"row": 3, "col": 3, "direction": "up"},
        {"row": 4, "col": 3, "direction": "down"},
        {"row": 4, "col": 4, "direction": "right"},
        {"row": 4, "col": 5, "direction": "right"},
    ],

    # 第 3 关
    [
        {"row": 0, "col": 0, "direction": "left"},
        {"row": 0, "col": 2, "direction": "right"},
        {"row": 0, "col": 4, "direction": "right"},
        {"row": 1, "col": 4, "direction": "down"},
        {"row": 2, "col": 4, "direction": "down"},
        {"row": 3, "col": 4, "direction": "left"},
        {"row": 3, "col": 3, "direction": "left"},
        {"row": 3, "col": 2, "direction": "up"},
        {"row": 4, "col": 2, "direction": "down"},
        {"row": 5, "col": 2, "direction": "down"},
    ],

    # 第 4 关
    [
        {"row": 0, "col": 0, "direction": "right"},
        {"row": 0, "col": 3, "direction": "down"},
        {"row": 1, "col": 1, "direction": "up"},
        {"row": 1, "col": 4, "direction": "left"},
        {"row": 2, "col": 2, "direction": "down"},
        {"row": 2, "col": 5, "direction": "left"},
        {"row": 3, "col": 0, "direction": "up"},
        {"row": 3, "col": 3, "direction": "right"},
        {"row": 4, "col": 1, "direction": "down"},
        {"row": 4, "col": 4, "direction": "up"},
        {"row": 5, "col": 2, "direction": "left"},
        {"row": 5, "col": 5, "direction": "right"},
    ],

        # 第 5 关
    [
        {"row": 0, "col": 0, "direction": "right"},
        {"row": 0, "col": 3, "direction": "down"},
        {"row": 1, "col": 1, "direction": "up"},
        {"row": 1, "col": 4, "direction": "left"},
        {"row": 2, "col": 2, "direction": "right"},
        {"row": 2, "col": 5, "direction": "up"},
        {"row": 3, "col": 0, "direction": "down"},
        {"row": 3, "col": 3, "direction": "left"},
        {"row": 4, "col": 1, "direction": "right"},
        {"row": 4, "col": 4, "direction": "down"},
        {"row": 5, "col": 2, "direction": "left"},
        {"row": 5, "col": 5, "direction": "up"},
    ],
]
ROWS = 6
COLS = 6