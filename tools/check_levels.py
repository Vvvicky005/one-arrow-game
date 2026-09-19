"""
关卡体检工具。
检查 5 个关卡是否可解。
运行方式：
    python tools/check_levels.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.levels import LEVELS, ROWS, COLS
from core.solver import solve_level


def main():
    all_ok = True

    for i, level in enumerate(LEVELS):
        arrows = [
            {
                "row": d["row"],
                "col": d["col"],
                "direction": d["direction"],
                "active": True,
            }
            for d in level
        ]

        path = solve_level(ROWS, COLS, arrows)

        if path is None:
            print(f"第 {i + 1} 关：无解 ❌")
            all_ok = False
        else:
            print(f"第 {i + 1} 关：可解 ✅，点击顺序：{path}")

    if all_ok:
        print("\n全部关卡检查通过！")
    else:
        print("\n存在无解关卡，请调整关卡数据。")


if __name__ == "__main__":
    main()