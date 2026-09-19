"""
绘制工具。
"""

import math
import pygame
from ui import theme

def draw_text(surface, text, font, color, center):
    s = font.render(text, True, color)
    surface.blit(s, s.get_rect(center=center))

def draw_gradient_background(surface):
    for y in range(theme.HEIGHT):
        ratio = y / theme.HEIGHT
        r = int(theme.BG_TOP[0] * (1 - ratio) + theme.BG_BOTTOM[0] * ratio)
        g = int(theme.BG_TOP[1] * (1 - ratio) + theme.BG_BOTTOM[1] * ratio)
        b = int(theme.BG_TOP[2] * (1 - ratio) + theme.BG_BOTTOM[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (theme.WIDTH, y))

def draw_cloud(surface, x, y, scale=1):
    color = theme.WHITE
    pygame.draw.circle(surface, color, (int(x), int(y)), int(25 * scale))
    pygame.draw.circle(surface, color, (int(x + 30 * scale), int(y - 12 * scale)), int(32 * scale))
    pygame.draw.circle(surface, color, (int(x + 65 * scale), int(y)), int(24 * scale))
    pygame.draw.rect(surface, color, (int(x - 5 * scale), int(y), int(75 * scale), int(25 * scale)))

def draw_star(surface, x, y, radius, color):
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * 0.45
        points.append((x + math.cos(angle) * r, y + math.sin(angle) * r))
    pygame.draw.polygon(surface, color, points)

def draw_arrow_icon(surface, x, y, size, direction, color):
    cx, cy = x, y
    shaft_width = max(5, int(size * 0.14))
    shaft_length = size * 0.48

    if direction == "up":
        pygame.draw.rect(surface, color, (
            int(cx - shaft_width / 2), int(cy - size * 0.05),
            shaft_width, int(shaft_length)))
        points = [(cx, cy - size * 0.50),
                  (cx - size * 0.30, cy - size * 0.15),
                  (cx + size * 0.30, cy - size * 0.15)]
    elif direction == "down":
        pygame.draw.rect(surface, color, (
            int(cx - shaft_width / 2), int(cy - size * 0.43),
            shaft_width, int(shaft_length)))
        points = [(cx, cy + size * 0.50),
                  (cx - size * 0.30, cy + size * 0.15),
                  (cx + size * 0.30, cy + size * 0.15)]
    elif direction == "left":
        pygame.draw.rect(surface, color, (
            int(cx - size * 0.05), int(cy - shaft_width / 2),
            int(shaft_length), shaft_width))
        points = [(cx - size * 0.50, cy),
                  (cx - size * 0.15, cy - size * 0.30),
                  (cx - size * 0.15, cy + size * 0.30)]
    else:
        pygame.draw.rect(surface, color, (
            int(cx - size * 0.43), int(cy - shaft_width / 2),
            int(shaft_length), shaft_width))
        points = [(cx + size * 0.50, cy),
                  (cx + size * 0.15, cy - size * 0.30),
                  (cx + size * 0.15, cy + size * 0.30)]

    pygame.draw.polygon(surface, color, points)

def draw_mascot(surface, x, y):
    pygame.draw.circle(surface, theme.WHITE, (x, y), 58)
    pygame.draw.circle(surface, theme.BLUE, (x, y), 50)
    draw_arrow_icon(surface, x, y - 5, 65, "up", theme.WHITE)
    pygame.draw.circle(surface, theme.BLACK, (x - 17, y + 20), 5)
    pygame.draw.circle(surface, theme.BLACK, (x + 17, y + 20), 5)
    pygame.draw.circle(surface, theme.LIGHT_PINK, (x - 30, y + 30), 8)
    pygame.draw.circle(surface, theme.LIGHT_PINK, (x + 30, y + 30), 8)

def draw_button(surface, rect, text, mouse_pos, font, color=theme.BLUE):
    hover = rect.collidepoint(mouse_pos)
    draw_rect = rect.inflate(6, 6) if hover else rect

    pygame.draw.rect(surface, (190, 210, 230), draw_rect.move(0, 6), border_radius=20)
    pygame.draw.rect(surface, color, draw_rect, border_radius=20)

    highlight_rect = pygame.Rect(draw_rect.x + 8, draw_rect.y + 6,
                                 draw_rect.width - 16, 8)
    highlight_color = tuple(min(255, c + 30) for c in color)
    pygame.draw.rect(surface, highlight_color, highlight_rect, border_radius=5)

    if text == "开始游戏":
        arrow_x = draw_rect.centerx - 78
        arrow_y = draw_rect.centery
        play_points = [
            (arrow_x - 7, arrow_y - 12),
            (arrow_x - 7, arrow_y + 12),
            (arrow_x + 12, arrow_y),
        ]
        pygame.draw.polygon(surface, theme.WHITE, play_points)

        ts = font.render(text, True, theme.WHITE)
        surface.blit(ts, ts.get_rect(center=(draw_rect.centerx + 10, draw_rect.centery)))
    else:
        ts = font.render(text, True, theme.WHITE)
        surface.blit(ts, ts.get_rect(center=draw_rect.center))

def cell_center(row, col):
    x = theme.BOARD_X + col * theme.CELL_SIZE + theme.CELL_SIZE // 2
    y = theme.BOARD_Y + row * theme.CELL_SIZE + theme.CELL_SIZE // 2
    return x, y

def draw_board(surface):
    board_rect = pygame.Rect(
        theme.BOARD_X - 12, theme.BOARD_Y - 12,
        theme.COLS * theme.CELL_SIZE + 24,
        theme.ROWS * theme.CELL_SIZE + 24,
    )
    pygame.draw.rect(surface, theme.WHITE, board_rect, border_radius=25)
    pygame.draw.rect(surface, theme.CELL_BORDER, board_rect, width=2, border_radius=25)

    for row in range(theme.ROWS):
        for col in range(theme.COLS):
            rect = pygame.Rect(
                theme.BOARD_X + col * theme.CELL_SIZE + 3,
                theme.BOARD_Y + row * theme.CELL_SIZE + 3,
                theme.CELL_SIZE - 6,
                theme.CELL_SIZE - 6,
            )
            pygame.draw.rect(surface, theme.CELL_BG, rect, border_radius=15)
            pygame.draw.rect(surface, theme.CELL_BORDER, rect, width=1, border_radius=15)


def draw_arrow(surface, arrow):
    if not arrow["active"]:
        return

    if arrow["animating"]:
        x, y = arrow["draw_x"], arrow["draw_y"]
    else:
        x, y = cell_center(arrow["row"], arrow["col"])
        if arrow["shake"] > 0:
            offset = int(math.sin(arrow["shake"] * 50) * 6)
            x += offset

    color = arrow["color"]

    if arrow["flash"] > 0:
        flash_value = int(100 * abs(math.sin(arrow["flash"] * 12)))
        color = tuple(min(255, c + flash_value) for c in color)

    pygame.draw.circle(surface, theme.WHITE, (int(x), int(y)), 31)
    pygame.draw.circle(surface, color, (int(x), int(y)), 27)
    draw_arrow_icon(surface, x, y, 52, arrow["direction"], theme.WHITE)

def draw_particles(surface, particles):
    for p in particles:
        if p["life"] <= 0:
            continue
        pygame.draw.circle(surface, p["color"], (int(p["x"]), int(p["y"])), p["size"])