import pygame
import sys
import random
import os
from game.snake import Snake
from ai.controller import AIController
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('SNN Snake AI')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset()

    def reset(self):
        """Resets the game to its initial state."""
        self.snake1 = Snake(GREEN, (GRID_WIDTH // 4, GRID_HEIGHT // 2), (1, 0))
        self.snake2 = Snake(BLUE, (3 * GRID_WIDTH // 4, GRID_HEIGHT // 2), (-1, 0))

        self.ai1 = AIController(self, self.snake1)
        self.ai2 = AIController(self, self.snake2)

        self.food = self.spawn_food()
        self.score1 = 0
        self.score2 = 0
        self.game_over = False

    def spawn_food(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake1.body and pos not in self.snake2.body:
                return pos

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        if self.game_over:
            return

        # Get actions from AI controllers
        dir1 = self.ai1.get_action()
        self.snake1.change_direction(dir1)

        dir2 = self.ai2.get_action()
        self.snake2.change_direction(dir2)

        self.snake1.move()
        self.snake2.move()

        # Check for food
        if self.snake1.get_head() == self.food:
            self.snake1.grow()
            self.score1 += 1
            self.food = self.spawn_food()

        if self.snake2.get_head() == self.food:
            self.snake2.grow()
            self.score2 += 1
            self.food = self.spawn_food()

        # Check for collisions
        if self.check_collisions(self.snake1) or self.check_collisions(self.snake2):
            self.game_over = True

    def check_collisions(self, snake):
        head = snake.get_head()
        # Wall collision
        if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):
            return True
        # Self collision
        if snake.check_collision_with_self():
            return True
        # Collision with other snake
        other_snake = self.snake1 if snake == self.snake2 else self.snake2
        if head in other_snake.body:
            return True

        return False

    def draw(self):
        self.screen.fill(BLACK)
        self.snake1.draw(self.screen)
        self.snake2.draw(self.screen)
        # Draw food
        r = pygame.Rect((self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, RED, r)

        # Draw score
        score_text = self.font.render(f"P1: {self.score1}  P2: {self.score2}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            game_over_text = self.font.render("Game Over", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop with automatic restart."""
        while True: # Loop forever until user quits
            self.handle_input()
            self.update() # This will set game_over to True if a collision happens
            self.draw()

            if self.game_over:
                # Pause for 2 seconds to show the "Game Over" screen
                end_time = pygame.time.get_ticks() + 2000
                while pygame.time.get_ticks() < end_time:
                    self.handle_input() # Must keep handling quit events
                    self.draw()
                    self.clock.tick(10)

                self.reset() # Reset the game for a new round

            self.clock.tick(10)
