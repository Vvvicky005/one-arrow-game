"""
关卡求解与可通关性校验。
使用 BFS 搜索一个合法点击顺序。
"""
from collections import deque
from core.board import is_blocked

def solve_level(rows, cols, arrows, max_states=200000):
    """
    返回一个点击顺序列表，元素为 (row, col)；
    无解返回 None。
    """

    def make_state(arrow_list):
        return tuple(sorted(
            (a["row"], a["col"], a["direction"])
            for a in arrow_list if a["active"]
        ))

    start = make_state(arrows)
    queue = deque()
    queue.append((start, []))
    visited = {start}

    while queue:
        state, path = queue.popleft()

        if not state:
            return path

        arrows_state = [
            {"row": r, "col": c, "direction": d, "active": True}
            for r, c, d in state
        ]

        for arrow in arrows_state:
            if not is_blocked(arrow, arrows_state, rows, cols):
                new_arrows = [a for a in arrows_state if a is not arrow]
                new_state = make_state(new_arrows)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [(arrow["row"], arrow["col"])]))
                    if len(visited) > max_states:
                        return None

    return None

def is_solvable(rows, cols, arrows):
    return solve_level(rows, cols, arrows) is not None