init python:
    import enum
    import pygame_sdl2 as pygame
    import random
    import re
    import time

    def delete_all_saves():
        for slot in renpy.list_saved_games(fast=True):
            renpy.unlink_save(slot)    