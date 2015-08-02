from gamelib import launcher
import pygame

def main():
    pygame.init()
    engine = launcher.Engine()
    engine.runGame(30)


if __name__ == '__main__':
    main()