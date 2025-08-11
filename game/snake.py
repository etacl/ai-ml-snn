import pygame
from config import *

class Snake:
    def __init__(self, color, initial_pos, initial_dir):
        self.body = [initial_pos]
        for _ in range(SNAKE_INITIAL_LENGTH - 1):
            self.grow()
        self.direction = initial_dir
        self.color = color

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def change_direction(self, new_direction):
        # Prevent the snake from reversing
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def get_head(self):
        return self.body[0]

    def check_collision_with_self(self):
        head = self.get_head()
        return head in self.body[1:]

    def draw(self, surface):
        for segment in self.body:
            r = pygame.Rect((segment[0] * GRID_SIZE, segment[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)
