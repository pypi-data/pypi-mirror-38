import pygame
from game import Game
from gameobject import TestObject

pygame.init()

def run_game():
    game = Game()

    game.register_gameobject(TestObject(100, 50))

    while not game.close_requested:
        game.handle_events()

        if game.loop:
            game.update()
            game.draw()

        game.tick(60)

    pygame.quit()
    quit()

if __name__ == "__main__":
    run_game()
