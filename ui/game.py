"""
场景管理与主循环。
"""

import sys
import pygame

from ui import theme
from ui import render
from ui import animations
from core.board import is_blocked
from core.levels import LEVELS, ROWS, COLS

SCREEN_START = "start"
SCREEN_LEVEL_SELECT = "level_select"
SCREEN_GAME = "game"
SCREEN_HELP = "help"
SCREEN_LEVEL_CLEAR = "level_clear"
SCREEN_SUCCESS = "success"
SCREEN_FAIL = "fail"

# 5 个关卡的名字
LEVEL_NAMES = ["入门", "简单", "中等", "困难", "挑战"]


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((theme.WIDTH, theme.HEIGHT))
        pygame.display.set_caption("一箭又一箭")
        self.clock = pygame.time.Clock()

        self.current_screen = SCREEN_START
        self.current_level = 0
        self.mistakes = theme.MAX_MISTAKES
        self.score = 0
        self.level_start_time = 0
        self.hint_used = False

        self.message_text = ""
        self.message_timer = 0
        self.shake_timer = 0

        self.particles = []
        self.arrows = []

        # 背景音乐
        self.bgm_playing = False
        self.load_bgm()

    def load_bgm(self):
        """加载背景音乐，如果文件不存在就跳过"""
        import os
        bgm_path = os.path.join("assets", "bgm.mp3")
        if os.path.exists(bgm_path):
            try:
                pygame.mixer.music.load(bgm_path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                self.bgm_playing = True
            except Exception as e:
                print("背景音乐加载失败：", e)
                self.bgm_playing = False
        else:
            print("未找到 assets/bgm.mp3，跳过背景音乐。")
            self.bgm_playing = False

    # ==================== 关卡 ====================
    def load_level(self, index):
        self.arrows = []
        self.particles = []

        for i, data in enumerate(LEVELS[index]):
            self.arrows.append({
                "row": data["row"],
                "col": data["col"],
                "direction": data["direction"],
                "color": theme.ARROW_COLORS[i % len(theme.ARROW_COLORS)],
                "active": True,
                "animating": False,
                "anim_progress": 0.0,
                "start_x": 0, "start_y": 0,
                "target_x": 0, "target_y": 0,
                "draw_x": 0, "draw_y": 0,
                "shake": 0,
                "flash": 0,
            })

        self.mistakes = theme.MAX_MISTAKES
        self.hint_used = False
        self.level_start_time = pygame.time.get_ticks()
        self.message_text = ""
        self.message_timer = 0

    # ==================== 事件 ====================
    def handle_click(self, pos):
        if self.current_screen == SCREEN_START:
            self._click_start(pos)
        elif self.current_screen == SCREEN_LEVEL_SELECT:
            self._click_level_select(pos)
        elif self.current_screen == SCREEN_HELP:
            self._click_help(pos)
        elif self.current_screen == SCREEN_GAME:
            self._click_game(pos)
        elif self.current_screen == SCREEN_LEVEL_CLEAR:
            self._click_level_clear(pos)
        elif self.current_screen == SCREEN_SUCCESS:
            self._click_success(pos)
        elif self.current_screen == SCREEN_FAIL:
            self._click_fail(pos)

    def _click_start(self, pos):
        start_button = pygame.Rect(300, 480, 300, 75)
        level_button = pygame.Rect(250, 570, 180, 55)
        help_button = pygame.Rect(470, 570, 180, 55)

        if start_button.collidepoint(pos):
            self.current_level = 0
            self.score = 0
            self.load_level(self.current_level)
            self.current_screen = SCREEN_GAME
        elif level_button.collidepoint(pos):
            self.current_screen = SCREEN_LEVEL_SELECT
        elif help_button.collidepoint(pos):
            self.current_screen = SCREEN_HELP

    def _click_level_select(self, pos):
        card_width, card_height, gap = 150, 245, 20
        total_width = card_width * len(LEVELS) + gap * (len(LEVELS) - 1)
        start_x = (theme.WIDTH - total_width) // 2
        card_y = 205

        for i in range(len(LEVELS)):
            rect = pygame.Rect(start_x + i * (card_width + gap),
                               card_y, card_width, card_height)
            if rect.collidepoint(pos):
                self.current_level = i
                self.score = 0
                self.load_level(self.current_level)
                self.current_screen = SCREEN_GAME
                return

        back_button = pygame.Rect(350, 535, 200, 55)
        if back_button.collidepoint(pos):
            self.current_screen = SCREEN_START

    def _click_help(self, pos):
        back_button = pygame.Rect(350, 585, 200, 55)
        if back_button.collidepoint(pos):
            self.current_screen = SCREEN_START

    def _click_game(self, pos):
        restart_button = pygame.Rect(210, 610, 160, 50)
        hint_button = pygame.Rect(385, 610, 130, 50)
        back_button = pygame.Rect(530, 610, 160, 50)

        if restart_button.collidepoint(pos):
            self.load_level(self.current_level)
        elif hint_button.collidepoint(pos):
            self.use_hint()
        elif back_button.collidepoint(pos):
            self.current_screen = SCREEN_START
        else:
            self.click_arrow(pos)

    def _click_level_clear(self, pos):
        next_button = pygame.Rect(300, 450, 300, 65)
        home_button = pygame.Rect(350, 540, 200, 50)
        if next_button.collidepoint(pos):
            self.current_level += 1
            self.load_level(self.current_level)
            self.current_screen = SCREEN_GAME
        elif home_button.collidepoint(pos):
            self.current_screen = SCREEN_START

    def _click_success(self, pos):
        restart_button = pygame.Rect(300, 510, 300, 65)
        home_button = pygame.Rect(350, 595, 200, 50)
        if restart_button.collidepoint(pos):
            self.current_level = 0
            self.score = 0
            self.load_level(self.current_level)
            self.current_screen = SCREEN_GAME
        elif home_button.collidepoint(pos):
            self.current_screen = SCREEN_START

    def _click_fail(self, pos):
        restart_button = pygame.Rect(300, 485, 300, 65)
        home_button = pygame.Rect(350, 570, 200, 50)
        if restart_button.collidepoint(pos):
            self.load_level(self.current_level)
            self.current_screen = SCREEN_GAME
        elif home_button.collidepoint(pos):
            self.current_screen = SCREEN_START

    # ==================== 点击箭头 ====================
    def click_arrow(self, mouse_pos):
        mx, my = mouse_pos
        for arrow in reversed(self.arrows):
            if not arrow["active"] or arrow["animating"]:
                continue
            cx, cy = render.cell_center(arrow["row"], arrow["col"])
            if (mx - cx) ** 2 + (my - cy) ** 2 <= 30 ** 2:
                if is_blocked(arrow, self.arrows, ROWS, COLS):
                    self.trigger_collision(arrow)
                else:
                    animations.start_arrow_fly(arrow)
                return

    def trigger_collision(self, arrow):
        self.mistakes -= 1
        self.score = max(0, self.score - theme.MISTAKE_SCORE)
        arrow["shake"] = 0.35
        arrow["flash"] = 0.35
        self.shake_timer = 0.25
        self.message_text = f"被挡住啦！ -{theme.MISTAKE_SCORE} 分"
        self.message_timer = 1.2
        animations.create_particles(
            self.particles,
            *render.cell_center(arrow["row"], arrow["col"]),
            theme.RED, 8
        )
        if self.mistakes <= 0:
            self.current_screen = SCREEN_FAIL

    # ==================== 提示 ====================
    def find_hint(self):
        for arrow in self.arrows:
            if not arrow["active"] or arrow["animating"]:
                continue
            if not is_blocked(arrow, self.arrows, ROWS, COLS):
                return arrow
        return None

    def use_hint(self):
        if self.hint_used:
            self.message_text = "本关提示已经使用过啦"
            self.message_timer = 1.5
            return
        hint = self.find_hint()
        if hint is None:
            self.message_text = "暂时没有可移动的箭头"
            self.message_timer = 1.5
            return
        self.hint_used = True
        self.score = max(0, self.score - theme.HINT_SCORE)
        hint["flash"] = 1.2
        self.message_text = f"看这个箭头！ -{theme.HINT_SCORE} 分"
        self.message_timer = 1.5

    # ==================== 更新 ====================
    def update_game(self, dt):
        if self.message_timer > 0:
            self.message_timer = max(0, self.message_timer - dt)
        if self.shake_timer > 0:
            self.shake_timer = max(0, self.shake_timer - dt)

        for arrow in self.arrows:
            if arrow["shake"] > 0:
                arrow["shake"] = max(0, arrow["shake"] - dt)
            if arrow["flash"] > 0:
                arrow["flash"] = max(0, arrow["flash"] - dt)

        animations.update_arrow_animation(
            self.arrows, dt, self.particles,
            lambda v: setattr(self, "score", self.score + v)
        )
        animations.update_particles(self.particles, dt)

        active_count = sum(1 for a in self.arrows if a["active"])
        if active_count == 0 and self.current_screen == SCREEN_GAME:
            if self.current_level >= len(LEVELS) - 1:
                self.current_screen = SCREEN_SUCCESS
            else:
                self.current_screen = SCREEN_LEVEL_CLEAR

    # ==================== 绘制 ====================
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.current_screen == SCREEN_START:
            self.draw_start_screen(mouse_pos)
        elif self.current_screen == SCREEN_LEVEL_SELECT:
            self.draw_level_select_screen(mouse_pos)
        elif self.current_screen == SCREEN_HELP:
            self.draw_help_screen(mouse_pos)
        elif self.current_screen == SCREEN_GAME:
            self.draw_game_screen(mouse_pos)
        elif self.current_screen == SCREEN_LEVEL_CLEAR:
            self.draw_level_clear_screen(mouse_pos)
        elif self.current_screen == SCREEN_SUCCESS:
            self.draw_success_screen(mouse_pos)
        elif self.current_screen == SCREEN_FAIL:
            self.draw_fail_screen(mouse_pos)

        render.draw_particles(self.screen, self.particles)

    def draw_start_screen(self, mouse_pos):
        render.draw_gradient_background(self.screen)
        render.draw_cloud(self.screen, 80, 110, 0.8)
        render.draw_cloud(self.screen, 730, 120, 1.0)
        render.draw_cloud(self.screen, 620, 560, 0.7)
        render.draw_star(self.screen, 130, 250, 10, theme.YELLOW)
        render.draw_star(self.screen, 780, 300, 12, theme.PINK)
        render.draw_star(self.screen, 110, 500, 8, theme.PURPLE)
        render.draw_arrow_icon(self.screen, 130, 390, 50, "right", theme.LIGHT_PINK)
        render.draw_arrow_icon(self.screen, 770, 450, 50, "left", theme.PURPLE)

        render.draw_text(self.screen, "一箭又一箭", theme.get_font(64),
                         theme.DARK_BLUE, (theme.WIDTH // 2, 105))
        render.draw_text(self.screen, "ARROW PUZZLE", theme.get_font(22),
                         (120, 150, 180), (theme.WIDTH // 2, 170))
        render.draw_mascot(self.screen, theme.WIDTH // 2, 285)
        render.draw_text(self.screen, "第 1 关", theme.get_font(24),
                         theme.PURPLE, (theme.WIDTH // 2, 370))
        render.draw_text(self.screen, "点击箭头，让它们找到自己的出口",
                         theme.get_font(18), (90, 110, 140),
                         (theme.WIDTH // 2, 420))

        # 开始游戏按钮
        render.draw_button(self.screen, pygame.Rect(300, 480, 300, 75),
                           "开始游戏", mouse_pos, theme.get_font(28), theme.BLUE)

        # 并排的两个按钮
        render.draw_button(self.screen, pygame.Rect(250, 570, 180, 55),
                           "选择关卡", mouse_pos, theme.get_font(24), theme.PURPLE)

        render.draw_button(self.screen, pygame.Rect(470, 570, 180, 55),
                           "怎么玩？", mouse_pos, theme.get_font(24), theme.PURPLE)
        render.draw_text(self.screen, "按空格键 静音 / 恢复音乐",
                 theme.get_font(16), (120, 130, 150),
                 (theme.WIDTH // 2, 650))

    def draw_level_select_screen(self, mouse_pos):
        render.draw_gradient_background(self.screen)
        render.draw_cloud(self.screen, 70, 100, 0.8)
        render.draw_cloud(self.screen, 735, 115, 0.9)
        render.draw_star(self.screen, 125, 250, 10, theme.YELLOW)
        render.draw_star(self.screen, 780, 290, 11, theme.PINK)

        render.draw_text(self.screen, "选择关卡", theme.get_font(64),
                         theme.DARK_BLUE, (theme.WIDTH // 2, 90))
        render.draw_text(self.screen, "选择一个关卡开始挑战", theme.get_font(18),
                         (90, 110, 140), (theme.WIDTH // 2, 145))

        card_width, card_height, gap = 150, 245, 20
        total_width = card_width * len(LEVELS) + gap * (len(LEVELS) - 1)
        start_x = (theme.WIDTH - total_width) // 2
        card_y = 205
        level_colors = [theme.BLUE, theme.PURPLE, theme.PINK,
                        theme.GREEN, theme.ORANGE]

        for i in range(len(LEVELS)):
            rect = pygame.Rect(start_x + i * (card_width + gap),
                               card_y, card_width, card_height)

            hover = rect.collidepoint(mouse_pos)
            draw_rect = rect.inflate(8, 8) if hover else rect

            pygame.draw.rect(self.screen, (190, 210, 230),
                             draw_rect.move(0, 7), border_radius=25)
            pygame.draw.rect(self.screen, theme.WHITE,
                             draw_rect, border_radius=25)
            pygame.draw.rect(self.screen, level_colors[i],
                             draw_rect, width=3, border_radius=25)

            pygame.draw.circle(self.screen, level_colors[i],
                               (draw_rect.centerx, draw_rect.y + 60), 32)

            render.draw_text(self.screen, str(i + 1), theme.get_font(34),
                             theme.WHITE, (draw_rect.centerx, draw_rect.y + 60))
            render.draw_text(self.screen, f"第 {i + 1} 关", theme.get_font(24),
                             theme.DARK_BLUE, (draw_rect.centerx, draw_rect.y + 120))
            render.draw_text(self.screen, LEVEL_NAMES[i], theme.get_font(18),
                             level_colors[i], (draw_rect.centerx, draw_rect.y + 155))
            render.draw_text(self.screen, f"{len(LEVELS[i])} 个箭头",
                             theme.get_font(18), theme.BLACK,
                             (draw_rect.centerx, draw_rect.y + 195))

        render.draw_button(self.screen, pygame.Rect(350, 535, 200, 55),
                           "返回主页", mouse_pos, theme.get_font(28), theme.PURPLE)

    def draw_help_screen(self, mouse_pos):
        render.draw_gradient_background(self.screen)
        render.draw_cloud(self.screen, 80, 100, 0.8)
        render.draw_cloud(self.screen, 730, 110, 0.8)

        render.draw_text(self.screen, "怎么玩？", theme.get_font(64),
                         theme.DARK_BLUE, (theme.WIDTH // 2, 90))

        panel = pygame.Rect(160, 160, 580, 390)
        pygame.draw.rect(self.screen, theme.WHITE, panel, border_radius=30)
        pygame.draw.rect(self.screen, theme.CELL_BORDER, panel,
                         width=2, border_radius=30)

        rules = [
            "① 点击一个箭头",
            "② 箭头前方没有其他箭头，就可以飞出去",
            "③ 如果被其他箭头挡住，就无法移动",
            "④ 点击被挡住的箭头会扣分并消耗一次失误",
            "⑤ 清除所有箭头即可通关",
            "⑥ 失误次数用完则挑战失败",
        ]
        y = 215
        for rule in rules:
            render.draw_text(self.screen, rule, theme.get_font(22),
                             theme.BLACK, (theme.WIDTH // 2, y))
            y += 50

        render.draw_button(self.screen, pygame.Rect(350, 585, 200, 55),
                           "返回", mouse_pos, theme.get_font(28), theme.PURPLE)

    def draw_game_screen(self, mouse_pos):
        render.draw_gradient_background(self.screen)

        elapsed = (pygame.time.get_ticks() - self.level_start_time) // 1000
        time_text = f"时间：{elapsed // 60:02d}:{elapsed % 60:02d}"

        render.draw_text(self.screen, "一箭又一箭", theme.get_font(34),
                         theme.DARK_BLUE, (theme.WIDTH // 2, 42))
        render.draw_text(self.screen, f"第 {self.current_level + 1} / {len(LEVELS)} 关",
                         theme.get_font(22), theme.PURPLE, (120, 45))
        render.draw_text(self.screen, time_text, theme.get_font(18),
                         theme.DARK_BLUE, (620, 42))

        render.draw_text(self.screen, "失误", theme.get_font(18),
                         theme.BLACK, (735, 28))
        for i in range(theme.MAX_MISTAKES):
            x = 785 + i * 25
            color = theme.RED if i < self.mistakes else (220, 225, 235)
            pygame.draw.circle(self.screen, color, (x, 42), 8)

        render.draw_board(self.screen)
        for arrow in self.arrows:
            render.draw_arrow(self.screen, arrow)

        render.draw_button(self.screen, pygame.Rect(210, 610, 160, 50),
                           "重新开始", mouse_pos, theme.get_font(28), theme.BLUE)
        render.draw_button(self.screen, pygame.Rect(385, 610, 130, 50),
                           "提示", mouse_pos, theme.get_font(28), theme.ORANGE)
        render.draw_button(self.screen, pygame.Rect(530, 610, 160, 50),
                           "返回主页", mouse_pos, theme.get_font(28), theme.PURPLE)

        if self.message_timer > 0:
            color = theme.RED if "挡" in self.message_text else theme.DARK_BLUE
            render.draw_text(self.screen, self.message_text, theme.get_font(22),
                             color, (theme.WIDTH // 2, 575))

        render.draw_text(self.screen, f"得分：{self.score}", theme.get_font(18),
                         theme.BLACK, (100, 635))

    def draw_level_clear_screen(self, mouse_pos):
        render.draw_gradient_background(self.screen)
        render.draw_text(self.screen, "关卡完成！", theme.get_font(52),
                         theme.GREEN, (theme.WIDTH // 2, 150))
        render.draw_text(self.screen, f"第 {self.current_level + 1} 关完成",
                         theme.get_font(34), theme.DARK_BLUE, (theme.WIDTH // 2, 240))
        render.draw_text(self.screen, "准备进入下一关", theme.get_font(22),
                         theme.BLACK, (theme.WIDTH // 2, 310))
        render.draw_text(self.screen, f"当前得分：{self.score}",
                         theme.get_font(22), theme.PURPLE, (theme.WIDTH // 2, 365))

        render.draw_button(self.screen, pygame.Rect(300, 450, 300, 65),
                           "下一关", mouse_pos, theme.get_font(28), theme.GREEN)
        render.draw_button(self.screen, pygame.Rect(350, 540, 200, 50),
                           "返回主页", mouse_pos, theme.get_font(28), theme.PURPLE)

    def draw_success_screen(self, mouse_pos):
        render.draw_gradient_background(self.screen)
        render.draw_cloud(self.screen, 100, 110, 0.8)
        render.draw_cloud(self.screen, 720, 120, 0.8)
        render.draw_star(self.screen, 150, 300, 14, theme.YELLOW)
        render.draw_star(self.screen, 760, 330, 14, theme.YELLOW)
        render.draw_star(self.screen, 210, 520, 14, theme.YELLOW)
        render.draw_star(self.screen, 690, 500, 14, theme.YELLOW)

        render.draw_text(self.screen, "全部通关！", theme.get_font(52),
                         theme.DARK_BLUE, (theme.WIDTH // 2, 150))
        render.draw_text(self.screen, "太厉害啦！", theme.get_font(34),
                         theme.PURPLE, (theme.WIDTH // 2, 230))
        render.draw_mascot(self.screen, theme.WIDTH // 2, 350)
        render.draw_text(self.screen, f"最终得分：{self.score}",
                         theme.get_font(22), theme.BLACK, (theme.WIDTH // 2, 445))

        render.draw_button(self.screen, pygame.Rect(300, 510, 300, 65),
                           "再玩一次", mouse_pos, theme.get_font(28), theme.GREEN)
        render.draw_button(self.screen, pygame.Rect(350, 595, 200, 50),
                           "返回主页", mouse_pos, theme.get_font(28), theme.PURPLE)

    def draw_fail_screen(self, mouse_pos):
        render.draw_gradient_background(self.screen)
        render.draw_text(self.screen, "挑战失败", theme.get_font(52),
                         theme.RED, (theme.WIDTH // 2, 150))
        render.draw_text(self.screen, "别灰心，再试一次吧！",
                         theme.get_font(34), theme.PURPLE, (theme.WIDTH // 2, 225))

        pygame.draw.circle(self.screen, theme.WHITE, (theme.WIDTH // 2, 350), 70)
        pygame.draw.circle(self.screen, theme.LIGHT_PINK, (theme.WIDTH // 2, 350), 60)
        pygame.draw.line(self.screen, theme.RED,
                         (theme.WIDTH // 2 - 25, 325),
                         (theme.WIDTH // 2 + 25, 375), 8)
        pygame.draw.line(self.screen, theme.RED,
                         (theme.WIDTH // 2 + 25, 325),
                         (theme.WIDTH // 2 - 25, 375), 8)

        render.draw_text(self.screen, f"当前得分：{self.score}",
                         theme.get_font(22), theme.BLACK, (theme.WIDTH // 2, 430))

        render.draw_button(self.screen, pygame.Rect(300, 485, 300, 65),
                           "重新挑战", mouse_pos, theme.get_font(28), theme.BLUE)
        render.draw_button(self.screen, pygame.Rect(350, 570, 200, 50),
                           "返回主页", mouse_pos, theme.get_font(28), theme.PURPLE)

    # ==================== 主循环 ====================
    def run(self):
        while True:
            dt = self.clock.tick(theme.FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

                elif event.type == pygame.KEYDOWN:
                    # ESC 返回主页
                    if event.key == pygame.K_ESCAPE and self.current_screen != SCREEN_START:
                        self.current_screen = SCREEN_START

                    # R 重新开始当前关卡
                    if event.key == pygame.K_r and self.current_screen == SCREEN_GAME:
                        self.load_level(self.current_level)

                    # SPACE 静音 / 恢复音乐
                    if event.key == pygame.K_SPACE:
                        print("收到 M 键，bgm_playing =", self.bgm_playing)
                        if self.bgm_playing:
                            pygame.mixer.music.stop()
                            self.bgm_playing = False
                            print("音乐已停止")
                        else:
                            pygame.mixer.music.play(-1)
                            self.bgm_playing = True
                            print("音乐开始播放")

            if self.current_screen == SCREEN_GAME:
                self.update_game(dt)
            else:
                animations.update_particles(self.particles, dt)

            self.draw()
            pygame.display.flip()