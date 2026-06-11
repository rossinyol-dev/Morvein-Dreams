# Определение Python типов и функций
init python:
    import enum
    import pygame_sdl2 as pygame
    import random

    class STATE(enum.Enum):
        HEALTHY = "Здоров"
        INJURED = "Ранен"
        GRAVELY = "Умирает"
        DEAD = "Мертв"

    class PROF(enum.Enum):
        DOCTOR = "Доктор"
        MONK = "Монах"

    class Hero:
        def __init__(self, name, prof, state, humanity, will, aspect, control, dream, ord_rel, cult_rel, image, color):
            self.name = name
            self.prof = prof
            self.state = state
            self.humanity = humanity
            self.will = will
            self.aspect = aspect
            self.control = control
            self.ord_rel = ord_rel
            self.cult_rel = cult_rel
            self.image = image
            self.color = color
            self.dream = dream

    class Note(object):
        def __init__(self, note_id, title, text=""):
            self.id = note_id
            self.title = title
            self.text = text

    class InvItem(object):
        def __init__(self, item_id, title, icon, description, count):
            self.id = item_id
            self.title = title
            self.icon = icon
            self.description = description
            self.count = count

    # Настройки игры
    def delete_all_saves():
        for slot in renpy.list_saved_games(fast=True):
            renpy.unlink_save(slot)

    def pause_music():
        global saved_music_pos, saved_music_file

        saved_music_pos = renpy.music.get_pos("music")
        saved_music_file = renpy.music.get_playing("music")

        renpy.music.stop(channel="music", fadeout=1.0)

    def resume_music():
        if saved_music_file:
            renpy.music.play(
                saved_music_file,
                channel="music",
                loop=True,
                synchro_start=saved_music_pos,
                fadein=1.0
            )

    # Логические функци
    def passive_check(stat, min_value, text, altText, addDream):
        if(stat) >= min_value:
            renpy.sound.play("audio/fx/dream_fx.mp3") 

    def add_stat(hero_object, stat_name, value):
        current_value = getattr(hero_object, stat_name)
        setattr(hero_object, stat_name, current_value + value)
        renpy.sound.play("audio/fx/pass_fx.mp3")

    def debuff_stats(hero):
        isDebuffed: True
        hero.humanity -= 1
        hero.will -= 1
        hero.aspect -= 1
        hero.control -= 1
    
    def heal_debuff(hero):
        if (isDebuffed):
            hero.humanity += 1
            hero.will += 1
            hero.aspect += 1
            hero.control += 1
    
    def reduce_dream(hero):
        hero.dream =- 1

    # Эффекты
    def start_dream_effect():
        pause_music()
        renpy.sound.play("audio/fx/horror_bell.mp3")
        renpy.music.play(
            "audio/dream_theme.mp3",
            fadein=2.0
        )
        renpy.layer_at_list([slow_shaking], layer="master")

    def stop_dream_effect():
        renpy.layer_at_list([], layer="master")
        renpy.music.stop(fadeout=2.0)
        resume_music()

    def check_dream(min_value, text):
        if hero.dream > min_value:
            # Начинаем отображение сна
            renpy.transition(fade)
            renpy.sound.play("audio/fx/dream_fx.mp3") 
            
            # Трясем экран
            renpy.show("black", layer="bottom") 
            renpy.layer_at_list([slow_shaking], layer='master')
            renpy.say(None, f"{{=dream_style}}{text}{{/=dream_style}}", interact=True)
            renpy.layer_at_list([], layer='master')
            renpy.hide("black", layer="master")
            
            # Завершаем отображение сна
            renpy.transition(fade)

    def dream_glitch(text, level):
        if level < 3:
            return text

        chars = list(text)
        symbols = [
            "☽", 
            "☾",
            "✧", 
            "✦",
            "◈",
            "⊙",
            "∅",
            "ꙮ",
            "⸸",
            "◌",
            "🜄",
        ]

        chance = 0.03 * level

        for i, ch in enumerate(chars):
            if ch != " " and random.random() < chance:
                chars[i] = random.choice(symbols)

        return "".join(chars)


