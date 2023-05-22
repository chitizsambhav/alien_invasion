import sys

import pygame


def check_event():
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            sys.exit()

