# Shalom Yemane
# CPSC 386-01
# 2021-12-13
# syemane@csu.fullerton.edu
# @S-Yemane
#
# Lab 05-00
#
# This file is the game controller.
#

import pygame
import scene


def display_info():
    """Print out the information about the display driver and video information."""
    print(
        'The display is using "{}" driver.'.format(pygame.display.get_driver())
    )
    print('Video Info:')
    print(pygame.display.Info())


class InvadersGame:
    """Operates the Space Invaders Game."""

    def __init__(self):
        pass

    def run(self):
        """This is the entry point to the game. It is the main function!"""
        if not pygame.font:
            print('Warning: Fonts disabled.')
        if not pygame.mixer:
            print('Warning: Sound disabled.')
        pygame.init()
        display_info()
        window_size = (800, 800)
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(window_size)
        title = 'Invaders'
        pygame.display.set_caption(title)

        pygame.mixer.init()
        pygame.mixer.music.load('GameTheme.ogg')
        pygame.mixer.music.play(-1)

        scene_list = [
            scene.TitleScene(screen, (0, 0, 0)),
            scene.GameScene(screen, (0, 0, 0)),
            scene.GameOverScene(screen, (0, 0, 0)),
        ]

        current_scene = scene_list[0]
        current_scene.start()
        while current_scene.game_is_valid():
            while current_scene.is_valid():
                clock.tick(current_scene.framerate())
                for event in pygame.event.get():
                    current_scene.process_event(event)
                    pygame.display.update()
                current_scene.update()
                current_scene.draw()
                pygame.display.update()

            current_scene.end()
            if current_scene.go_to_title_screen():
                current_scene = scene_list[0]
            elif current_scene.go_to_game_screen():
                current_scene = scene_list[1]
            elif current_scene.go_to_game_over_screen():
                current_scene = scene_list[2]
                current_scene.load_score(scene_list[1].get_score())
            else:
                pygame.quit()
                return 0
            current_scene.reset_flags()
            current_scene.start()
        print('Exiting')
        pygame.quit()

        return 0
