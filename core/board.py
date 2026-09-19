"""
棋盘核心逻辑。
不依赖 pygame，可独立测试。
"""
DIRECTIONS = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}

def find_arrow(arrows, row, col):
    """查找某个格子上的箭头"""
    for arrow in arrows:
        if arrow["active"] and arrow["row"] == row and arrow["col"] == col:
            return arrow
    return None

def is_blocked(arrow, arrows, rows, cols):
    """判断箭头前方是否被阻挡"""
    row = arrow["row"]
    col = arrow["col"]
    dr, dc = DIRECTIONS[arrow["direction"]]
    r = row + dr
    c = col + dc

    while 0 <= r < rows and 0 <= c < cols:
        for other in arrows:
            if not other["active"]:
                continue
            if other is arrow:
                continue
            if other["row"] == r and other["col"] == c:
                return True
        r += dr
        c += dc

    return False

def can_fly_out(arrow, arrows, rows, cols):
    """能否飞出"""
    return not is_blocked(arrow, arrows, rows, cols)

def click(arrows, row, col, rows, cols):
    """
    返回 ("empty"|"fly"|"blocked", arrow)
    """
    arrow = find_arrow(arrows, row, col)
    if arrow is None:
        return "empty", None
    if can_fly_out(arrow, arrows, rows, cols):
        return "fly", arrow
    return "blocked", arrow

def is_clear(arrows):
    """是否全部清空"""
    return all(not a["active"] for a in arrows)

def remaining(arrows):
    """剩余箭头数量"""
    return sum(1 for a in arrows if a["active"])