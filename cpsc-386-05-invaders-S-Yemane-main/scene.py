# Shalom Yemane
# CPSC 386-01
# 2021-12-13
# syemane@csu.fullerton.edu
# @S-Yemane
#
# Lab 05-00
#
# This file is in charge of drawing to the screen.
#

import pygame
import random
from enemy import Enemy

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Scene:
    """The default Scene class."""

    def __init__(self, screen, background_color):
        self._is_valid = True
        self._game_is_valid = True
        self._go_to_title_screen = False
        self._go_to_game_screen = False
        self._go_to_game_over_screen = False
        self._framerate = 60
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background_color = background_color
        self._background.fill(self._background_color)
        self._font = pygame.freetype.SysFont('arial', 24)

    def is_valid(self):
        """Returns whether the current scene should continue to be displayed or not."""
        return self._is_valid

    def game_is_valid(self):
        """Returns whether the game is being exited out of or not."""
        return self._game_is_valid

    def go_to_title_screen(self):
        """Returns if the next scene should be the title screen."""
        return self._go_to_title_screen

    def go_to_game_screen(self):
        """Returns if the next scene should be the title screen."""
        return self._go_to_game_screen

    def go_to_game_over_screen(self):
        """Returns if the next scene should be the title screen."""
        return self._go_to_game_over_screen

    def reset_flags(self):
        """Resets all the boolean flags to default values."""
        self._is_valid = True
        self._game_is_valid = True
        self._go_to_title_screen = False
        self._go_to_game_screen = False

    def framerate(self):
        """Returns the framerate."""
        return self._framerate

    def start(self):
        """Start the scene."""
        pass

    def end(self):
        """End the scene."""
        pass

    def update(self):
        """Update the scene."""
        pass

    def draw(self):
        """Draws onto the window screen."""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Processes a given event for potential input/actions."""
        if event.type == pygame.QUIT:
            print('Quit')
            self._is_valid = False
            self._game_is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print('Quit')
            self._is_valid = False
            self._game_is_valid = False


class TitleScene(Scene):
    """The Title Scene class."""

    def __init__(self, screen, background_color):
        super().__init__(screen, background_color)
        self._start_button = pygame.Rect(350, 500, 100, 50)
        self._quit_button = pygame.Rect(350, 600, 100, 50)

    def draw(self):
        super().draw()
        title_surface, unused_rect = self._font.render('Invaders', WHITE)
        start_button_surface, unused_rect = self._font.render('Start', BLACK)
        quit_button_surface, unused_rect = self._font.render('Quit', BLACK)
        self._screen.blit(title_surface, (350, 250))
        pygame.draw.rect(self._screen, WHITE, self._start_button)
        pygame.draw.rect(self._screen, WHITE, self._quit_button)
        self._screen.blit(
            start_button_surface,
            (self._start_button.x + 25, self._start_button.y + 15),
        )
        self._screen.blit(
            quit_button_surface,
            (self._quit_button.x + 27, self._quit_button.y + 15),
        )

    def process_event(self, event):
        super().process_event(event)
        # Hitting the "Enter" key starts the game.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._is_valid = False
            self._go_to_game_screen = True
        # Handling for clicking on the title screen buttons.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseposition = pygame.mouse.get_pos()
            if self._start_button.collidepoint(mouseposition):
                self._is_valid = False
                self._go_to_game_screen = True
            if self._quit_button.collidepoint(mouseposition):
                self._is_valid = False
                self._game_is_valid = False


class GameScene(Scene):
    """The Game Scene class."""

    def __init__(self, screen, background_color):
        super().__init__(screen, background_color)
        self._is_playing = True
        self._button_font = pygame.freetype.SysFont('arial', 12)
        self._shoot_button = pygame.Rect(375, 700, 50, 25)
        self._left_button = pygame.Rect(300, 700, 50, 25)
        self._right_button = pygame.Rect(450, 700, 50, 25)
        self._player_coords = (400, 600)
        self._player_movement_speed = 20
        self._player_rect = pygame.Rect(
            self._player_coords[0] - 10, self._player_coords[1] - 10, 20, 20
        )
        self._score = 0
        self._lives = 3

        self._obstacle_one_rect = pygame.Rect(150, 550, 100, 20)
        self._obstacle_two_rect = pygame.Rect(550, 550, 100, 20)

        self._sound_effect_channel = pygame.mixer.Channel(1)
        self._laser_sound = pygame.mixer.Sound('sf_laser_14.mp3')

        self._player_laser_exists = False
        self._player_laser = None
        self._player_laser_rect = None
        self._enemy_laser_exists = False
        self._enemy_laser = None
        self._enemy_laser_rect = None

        self._enemies = []
        self._leading_enemies = []
        self.spawn_enemies()

    def update(self):
        if self._is_playing:
            self.move_enemies()
            self.move_lasers()
            self.enemy_attack()
            self.check_for_collision()

    def draw(self):
        super().draw()
        self.draw_bounds()
        self.draw_buttons()
        self.draw_obstacles()
        self.draw_player()
        self.draw_enemies()
        self.draw_lasers()
        self.draw_score()

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseposition = pygame.mouse.get_pos()
            if (
                self._shoot_button.collidepoint(mouseposition)
                and not self._player_laser_exists
            ):
                self._player_laser = (
                    self._player_coords[0],
                    self._player_coords[1] - 20,
                )
                self._player_laser_rect = pygame.Rect(
                    self._player_laser[0] - 2, self._player_laser[1] - 5, 4, 10
                )
                self._sound_effect_channel.play(self._laser_sound)
                self._player_laser_exists = True
            if self._left_button.collidepoint(mouseposition):
                self._player_coords = (
                    self._player_coords[0] - self._player_movement_speed,
                    self._player_coords[1],
                )
                self._player_rect = pygame.Rect(
                    self._player_coords[0] - 10,
                    self._player_coords[1] - 10,
                    20,
                    20,
                )
            if self._right_button.collidepoint(mouseposition):
                self._player_coords = (
                    self._player_coords[0] + self._player_movement_speed,
                    self._player_coords[1],
                )
                self._player_rect = pygame.Rect(
                    self._player_coords[0] - 10,
                    self._player_coords[1] - 10,
                    20,
                    20,
                )

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self._player_laser_exists:
                self._player_laser = (
                    self._player_coords[0],
                    self._player_coords[1] - 20,
                )
                self._player_laser_rect = pygame.Rect(
                    self._player_laser[0] - 2, self._player_laser[1] - 5, 4, 10
                )
                self._sound_effect_channel.play(self._laser_sound)
                self._player_laser_exists = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self._player_coords = (
                    self._player_coords[0] - self._player_movement_speed,
                    self._player_coords[1],
                )
                self._player_rect = pygame.Rect(
                    self._player_coords[0] - 10,
                    self._player_coords[1] - 10,
                    20,
                    20,
                )
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self._player_coords = (
                    self._player_coords[0] + self._player_movement_speed,
                    self._player_coords[1],
                )
                self._player_rect = pygame.Rect(
                    self._player_coords[0] - 10,
                    self._player_coords[1] - 10,
                    20,
                    20,
                )

    def get_score(self):
        return self._score

    def check_for_collision(self):
        """Check if the player or any enemy has died."""
        if self._player_laser_exists:
            if self._player_laser_rect.colliderect(
                self._obstacle_one_rect
            ) or self._player_laser_rect.colliderect(self._obstacle_two_rect):
                self._player_laser_exists = False
            else:
                for enemy in self._enemies:
                    if (
                        not enemy.destroyed
                        and self._player_laser_rect.colliderect(
                            enemy.get_rect()
                        )
                    ):
                        self._score += 1
                        self._player_laser_exists = False
                        index = self._enemies.index(enemy)
                        index2 = self._leading_enemies.index(index)
                        if index > 3:
                            self._leading_enemies[index2] -= 4
                        else:
                            self._leading_enemies.remove(index)
                        self._enemies[index].destroyed = True

                        if self._score % 16 == 0:
                            self.spawn_enemies()

        if self._enemy_laser_exists:
            if self._enemy_laser_rect.colliderect(
                self._obstacle_one_rect
            ) or self._enemy_laser_rect.colliderect(self._obstacle_two_rect):
                self._enemy_laser_exists = False
            elif self._enemy_laser_rect.colliderect(self._player_rect):
                self._enemy_laser_exists = False
                self._lives -= 1

                if self._lives <= 0:
                    self._is_playing = False
                    self._is_valid = False
                    self._go_to_game_over_screen = True

    def spawn_enemies(self):
        """Spawns in the enemies, both in game and in memory."""
        gridSize = 4
        self._enemies = []
        self._leading_enemies = []
        for y in range(0, gridSize):
            for x in range(0, gridSize):
                enemy = Enemy(
                    (
                        (250 + (300 / (gridSize - 1)) * x),
                        200 + (200 / (gridSize - 1)) * y,
                    )
                )
                self._enemies.append(enemy)
                if y == gridSize - 1:
                    self._leading_enemies.append(y * gridSize + x)

    def enemy_attack(self):
        """Chooses which enemy to shoot from, and when."""
        if not self._enemy_laser_exists:
            self._enemy_laser_exists = True
            enemy_index = random.randint(0, len(self._leading_enemies) - 1)
            self._enemy_laser = self._enemies[
                self._leading_enemies[enemy_index]
            ].get_position()
            self._enemy_laser = (
                self._enemy_laser[0],
                self._enemy_laser[1] + 20,
            )
            self._enemy_laser_rect = pygame.Rect(
                self._enemy_laser[0] - 2, self._enemy_laser[1] - 5, 4, 10
            )

            self._sound_effect_channel.play(self._laser_sound)

    def move_enemies(self):
        """Move all enemies"""
        for enemy in self._enemies:
            enemy.move(5 / self._framerate)

    def move_lasers(self):
        """Move the laser objects."""
        laser_movement_speed = 200 / self._framerate
        if self._enemy_laser_exists:
            self._enemy_laser = (
                self._enemy_laser[0],
                self._enemy_laser[1] + laser_movement_speed,
            )
            self._enemy_laser_rect = pygame.Rect(
                self._enemy_laser[0] - 2, self._enemy_laser[1] - 5, 4, 10
            )
            if self._enemy_laser[1] >= 650:
                self._enemy_laser_exists = False

        if self._player_laser_exists:
            self._player_laser = (
                self._player_laser[0],
                self._player_laser[1] - laser_movement_speed * 2,
            )
            self._player_laser_rect = pygame.Rect(
                self._player_laser[0] - 2, self._player_laser[1] - 5, 4, 10
            )
            if self._player_laser[1] <= 150:
                self._player_laser_exists = False

    def draw_bounds(self):
        """Draws a 500x500 box, acting as a playable area boundary."""
        pygame.draw.line(self._screen, WHITE, (150, 150), (150, 650))
        pygame.draw.line(self._screen, WHITE, (150, 650), (650, 650))
        pygame.draw.line(self._screen, WHITE, (650, 650), (650, 150))
        pygame.draw.line(self._screen, WHITE, (650, 150), (150, 150))

    def draw_buttons(self):
        """Draws 4 buttons for use in controlling the snake."""
        pygame.draw.rect(self._screen, WHITE, self._shoot_button)
        pygame.draw.rect(self._screen, WHITE, self._left_button)
        pygame.draw.rect(self._screen, WHITE, self._right_button)
        shoot_surface, rect = self._button_font.render('SHOOT', BLACK)
        left_surface, rect = self._button_font.render('LEFT', BLACK)
        right_surface, rect = self._button_font.render('RIGHT', BLACK)
        self._screen.blit(
            shoot_surface, (self._shoot_button.x + 4, self._shoot_button.y + 8)
        )
        self._screen.blit(
            left_surface, (self._left_button.x + 11, self._left_button.y + 8)
        )
        self._screen.blit(
            right_surface, (self._right_button.x + 8, self._right_button.y + 8)
        )

    def draw_player(self):
        """Draws all the individual parts of the snake."""
        pygame.draw.rect(self._screen, WHITE, self._player_rect)

    def draw_enemies(self):
        """Draw all the enemies."""
        for enemy in self._enemies:
            enemy.draw(self._screen)

    def draw_obstacles(self):
        """Draw the obstacles"""
        pygame.draw.rect(self._screen, WHITE, self._obstacle_one_rect)
        pygame.draw.rect(self._screen, WHITE, self._obstacle_two_rect)

    def draw_lasers(self):
        """Draw all the laser objects."""
        if self._enemy_laser_exists:
            pygame.draw.rect(self._screen, (255, 0, 0), self._enemy_laser_rect)
        if self._player_laser_exists:
            pygame.draw.rect(self._screen, WHITE, self._player_laser_rect)

    def draw_score(self):
        """Draws the scoreboard."""
        score_surface, rect = self._font.render(
            "LIVES: " + str(self._lives), WHITE
        )
        self._screen.blit(score_surface, (150, 700))
        score_surface, rect = self._font.render(
            "SCORE: " + str(self._score), WHITE
        )
        self._screen.blit(score_surface, (540, 700))


class GameOverScene(Scene):
    """The Game Over Screen."""

    def __init__(self, screen, background_color):
        super().__init__(screen, background_color)
        self._button_font = pygame.freetype.SysFont('arial', 12)
        self._game_over_font = pygame.freetype.SysFont('arial', 50)
        self._shoot_button = pygame.Rect(375, 700, 50, 25)
        self._left_button = pygame.Rect(300, 700, 50, 25)
        self._right_button = pygame.Rect(450, 700, 50, 25)
        self._game_over_panel = pygame.Rect(250, 250, 300, 300)
        self._score = 0

    def draw(self):
        super().draw()
        self.draw_bounds()
        self.draw_buttons()
        self.draw_score()
        self.draw_game_over()

    def process_event(self, event):
        super().process_event(event)

    def load_score(self, score):
        """Load the score from the game to keep up the display."""
        self._score = score

    def draw_game_over(self):
        """Write 'Game Over' on the screen."""
        pygame.draw.rect(self._screen, BLACK, self._game_over_panel)
        game_over_surface, rect = self._font.render('GAME OVER', WHITE)

        self._screen.blit(game_over_surface, (325, 370))

    def draw_bounds(self):
        """Draws a 500x500 box, acting as a playable area boundary."""
        pygame.draw.line(self._screen, WHITE, (150, 150), (150, 650))
        pygame.draw.line(self._screen, WHITE, (150, 650), (650, 650))
        pygame.draw.line(self._screen, WHITE, (650, 650), (650, 150))
        pygame.draw.line(self._screen, WHITE, (650, 150), (150, 150))

    def draw_buttons(self):
        """Draws 4 buttons for use in controlling the snake."""
        pygame.draw.rect(self._screen, WHITE, self._shoot_button)
        pygame.draw.rect(self._screen, WHITE, self._left_button)
        pygame.draw.rect(self._screen, WHITE, self._right_button)
        shoot_surface, rect = self._button_font.render('SHOOT', BLACK)
        left_surface, rect = self._button_font.render('LEFT', BLACK)
        right_surface, rect = self._button_font.render('RIGHT', BLACK)
        self._screen.blit(
            shoot_surface, (self._shoot_button.x + 4, self._shoot_button.y + 8)
        )
        self._screen.blit(
            left_surface, (self._left_button.x + 11, self._left_button.y + 8)
        )
        self._screen.blit(
            right_surface, (self._right_button.x + 8, self._right_button.y + 8)
        )

    def draw_score(self):
        """Draws the scoreboard."""
        score_surface, rect = self._font.render("LIVES: 0", WHITE)
        self._screen.blit(score_surface, (150, 700))
        score_surface, rect = self._font.render(
            "SCORE: " + str(self._score), WHITE
        )
        self._screen.blit(score_surface, (540, 700))
