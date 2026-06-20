init python:
    import enum
    import pygame_sdl2 as pygame
    import random
    import re
    import time

    config.layers = [ "background", "master", "transient", "screens", "overlay" ]

    class STATE(enum.Enum):
        HEALTHY = "Здоров"
        INJURED = "Ранен"
        GRAVELY = "Умирает"
        DEAD = "Мертв"

    class PROF(enum.Enum):
        DOCTOR = "Доктор"
        MONK = "Монах"

    class Hero:
        def __init__(self, name, full_name, prof, state, mercy, reason, aspect, control, ord_rel, cult_rel, image, portrait, color):
            self.name = name
            self.full_name = full_name
            self.prof = prof
            self.state = state
            self.mercy = mercy
            self.reason = reason
            self.aspect = aspect
            self.control = control
            self.ord_rel = ord_rel
            self.cult_rel = cult_rel
            self.image = image
            self.portrait = portrait
            self.color = color

    def passive_check(stat, min_value, text, altText, addDream):
        if(stat) >= min_value:
            renpy.sound.play("audio/fx/dream_fx.mp3") 

    def add_stat(hero_object, stat_name, value):
        current_value = getattr(hero_object, stat_name)
        setattr(hero_object, stat_name, current_value + value)
        renpy.sound.play("audio/fx/pass_fx.mp3")
    
    def reduce_dream(hero):
        hero.aspect =- 1

    def debuff_stats(hero):
        isDebuffed: True
        hero.mercy -= 1
        hero.reason -= 1
        hero.aspect -= 1
        hero.control -= 1
    
    def heal_debuff(hero):
        if (isDebuffed):
            hero.mercy += 1
            hero.reason += 1
            hero.aspect += 1
            hero.control += 1