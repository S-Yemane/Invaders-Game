# Shalom Yemane
# CPSC 386-01
# 2021-12-13
# syemane@csu.fullerton.edu
# @S-Yemane
#
# Lab 05-00
#
# This file represents the enemies of the game.
#

import pygame
import math


class Enemy:
    """The Enemy class"""

    def __init__(self, position):
        self._position = position
        self._rect = pygame.Rect(
            self._position[0] - 10, self._position[1] - 10, 20, 20
        )

        self._horizontal_move_cd = 0

        self.destroyed = False

    def move(self, move_amount):
        """Increment the position of the enemy ship."""
        horizontal_move = move_amount
        self._horizontal_move_cd += move_amount
        self._position = (
            self._position[0]
            + horizontal_move * math.cos(self._horizontal_move_cd),
            self._position[1] + move_amount,
        )
        self._rect = pygame.Rect(
            self._position[0] - 10, self._position[1] - 10, 20, 20
        )

    def draw(self, screen):
        """Draw the enemy ship."""
        if not self.destroyed:
            pygame.draw.rect(screen, (255, 0, 0), self._rect)

    def blow_up(self):
        """Set the enemy as destroyed."""
        self.destroyed = True
        self._rect = None

    def get_position(self):
        """Return the position of the enemy ship."""
        return self._position

    def get_rect(self):
        """Return the rect of the enemy, for collision."""
        return self._rect
