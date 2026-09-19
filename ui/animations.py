"""
动画与粒子。
"""

import math
import random
from ui import theme
from ui.render import cell_center

def create_particles(particles, x, y, color, count=12):
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(40, 100)
        particles.append({
            "x": x, "y": y,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "life": random.uniform(0.4, 0.8),
            "color": color,
            "size": random.randint(3, 7),
        })

def update_particles(particles, dt):
    for p in particles[:]:
        p["x"] += p["vx"] * dt
        p["y"] += p["vy"] * dt
        p["vy"] += 100 * dt
        p["life"] -= dt
        if p["life"] <= 0:
            particles.remove(p)

def start_arrow_fly(arrow):
    arrow["animating"] = True
    arrow["anim_progress"] = 0.0

    start_x, start_y = cell_center(arrow["row"], arrow["col"])
    arrow["start_x"] = start_x
    arrow["start_y"] = start_y

    direction = arrow["direction"]
    if direction == "up":
        arrow["target_x"] = start_x
        arrow["target_y"] = -100
    elif direction == "down":
        arrow["target_x"] = start_x
        arrow["target_y"] = theme.HEIGHT + 100
    elif direction == "left":
        arrow["target_x"] = -100
        arrow["target_y"] = start_y
    else:
        arrow["target_x"] = theme.WIDTH + 100
        arrow["target_y"] = start_y


def update_arrow_animation(arrows, dt, particles, add_score):
    for arrow in arrows:
        if not arrow["animating"]:
            continue

        arrow["anim_progress"] += dt * 2.8
        progress = min(arrow["anim_progress"], 1)
        eased = 1 - (1 - progress) ** 3

        x = arrow["start_x"] + (arrow["target_x"] - arrow["start_x"]) * eased
        y = arrow["start_y"] + (arrow["target_y"] - arrow["start_y"]) * eased

        arrow["draw_x"] = x
        arrow["draw_y"] = y

        if progress >= 1:
            arrow["active"] = False
            arrow["animating"] = False
            add_score(theme.CORRECT_SCORE)
            create_particles(particles, arrow["target_x"], arrow["target_y"],
                             arrow["color"], 10)