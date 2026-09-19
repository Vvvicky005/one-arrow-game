"""
核心逻辑自动化测试。
运行方式：
    python tests/test_core.py
或：
    python -m pytest tests/test_core.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.board import is_blocked, can_fly_out, click, is_clear, remaining


def make(r, c, d):
    """创建一个测试用箭头"""
    return {"row": r, "col": c, "direction": d, "active": True}


# ============================================================
# T01 点击前方无阻挡的箭头 → 可以飞出
# ============================================================

def test_fly_out_no_block():
    arrows = [make(0, 0, "right")]
    assert can_fly_out(arrows[0], arrows, 6, 6) is True


# ============================================================
# T02 点击前方有阻挡的箭头 → 被阻挡
# ============================================================

def test_blocked_by_arrow():
    arrows = [make(0, 0, "right"), make(0, 3, "up")]
    assert is_blocked(arrows[0], arrows, 6, 6) is True


# ============================================================
# T03 边缘箭头朝外 → 正常飞出，不越界
# ============================================================

def test_edge_fly_out_right():
    arrows = [make(0, 5, "right")]
    assert can_fly_out(arrows[0], arrows, 6, 6) is True


def test_edge_fly_out_left():
    arrows = [make(0, 0, "left")]
    assert can_fly_out(arrows[0], arrows, 6, 6) is True


def test_edge_fly_out_up():
    arrows = [make(0, 0, "up")]
    assert can_fly_out(arrows[0], arrows, 6, 6) is True


def test_edge_fly_out_down():
    arrows = [make(5, 0, "down")]
    assert can_fly_out(arrows[0], arrows, 6, 6) is True


# ============================================================
# 四个方向的基本测试
# ============================================================

def test_direction_up():
    arrows = [make(3, 0, "up")]
    assert can_fly_out(arrows[0], arrows, 6, 6) is True


def test_direction_down():
    arrows = [make(3, 0, "down")]
    assert can_fly_out(arrows[0], arrows, 6, 6) is True


def test_direction_left():
    arrows = [make(0, 3, "left")]
    assert can_fly_out(arrows[0], arrows, 6, 6) is True


def test_direction_right():
    arrows = [make(0, 3, "right")]
    assert can_fly_out(arrows[0], arrows, 6, 6) is True


# ============================================================
# click 返回值测试
# ============================================================

def test_click_empty():
    arrows = [make(0, 0, "right")]
    result, arrow = click(arrows, 3, 3, 6, 6)
    assert result == "empty"
    assert arrow is None


def test_click_fly():
    arrows = [make(0, 0, "right")]
    result, arrow = click(arrows, 0, 0, 6, 6)
    assert result == "fly"
    assert arrow is not None


def test_click_blocked():
    arrows = [make(0, 0, "right"), make(0, 3, "up")]
    result, arrow = click(arrows, 0, 0, 6, 6)
    assert result == "blocked"
    assert arrow is not None


# ============================================================
# 剩余数量 / 清空判断
# ============================================================

def test_remaining_and_clear():
    arrows = [make(0, 0, "right"), make(0, 3, "up")]
    assert remaining(arrows) == 2
    assert is_clear(arrows) is False

    arrows[0]["active"] = False
    arrows[1]["active"] = False
    assert remaining(arrows) == 0
    assert is_clear(arrows) is True


# ============================================================
# 手动运行
# ============================================================

if __name__ == "__main__":
    test_fly_out_no_block()
    test_blocked_by_arrow()
    test_edge_fly_out_right()
    test_edge_fly_out_left()
    test_edge_fly_out_up()
    test_edge_fly_out_down()
    test_direction_up()
    test_direction_down()
    test_direction_left()
    test_direction_right()
    test_click_empty()
    test_click_fly()
    test_click_blocked()
    test_remaining_and_clear()
    print("所有测试通过！")