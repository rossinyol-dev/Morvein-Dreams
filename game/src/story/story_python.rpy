init python:
    import enum
    import pygame_sdl2 as pygame
    import random
    import re
    import time

    # Глобальные настройки оформления истории
    config.layers = [ "background", "master", "transient", "screens", "overlay" ]
    dream_alpha = 0.8
    dream_active = True
    dream_text_min_limit = 3
    greek_map = {
        "а": "α",
        "е": "ε",
        "з": "ζ",
        "и": "ι",
        "к": "κ",
        "м": "μ",
        "н": "η",
        "о": "ο",
        "р": "ρ",
        "с": "ς",
        "т": "τ",
        "у": "υ",
        "ф": "φ",
        "х": "χ",

        "А": "Α",
        "Е": "Ε",
        "З": "Ζ",
        "И": "Ι",
        "К": "Κ",
        "М": "Μ",
        "Н": "Η",
        "О": "Ο",
        "Р": "Ρ",
        "С": "Σ",
        "Т": "Τ",
        "У": "Υ",
        "Ф": "Φ",
        "Х": "Χ",
    }

    def start_dream_effect(finish_nightmare = True):
        if (finish_nightmare == True):
            pause_music()
            renpy.sound.play("audio/fx/horror_bell.mp3")
            renpy.music.play(
                "audio/dream_theme.mp3",
                fadein=2.0
            )
        renpy.show("black", layer="background")
        renpy.layer_at_list([slow_shaking], layer="master")

    def stop_dream_effect(finish_nightmare = True):
        if (finish_nightmare == True):
            renpy.music.stop(fadeout=2.0)
            resume_music()
        renpy.layer_at_list([], layer="master")

    def hard_fade(scene_name, delay=3.0, texts = None):
        renpy.stop_skipping()

        renpy.hide_screen("say")
        renpy.hide_screen("quick_menu")
        renpy.hide_screen("gui")

        renpy.scene(layer="screens")
        renpy.scene(layer="overlay")

        renpy.scene(layer="master")
        renpy.show("black", layer="master")
        renpy.with_statement(None)

        if texts:
            renpy.say(None, texts)

        renpy.pause(0.5, hard=True)

        renpy.show(scene_name, layer="master", at_list=[fade_in_from_black(delay)])
        renpy.pause(delay, hard=True)

    def dream_scene_dynamic(st, at, image_name):
        global dream_alpha

        dream_alpha += random.uniform(-0.05, 0.05)
        dream_alpha = max(0.4, min(0.6, dream_alpha))

        d = Composite(
            (1920, 1080),
            (0, 0), renpy.displayable(image_name),
            (0, 0), Transform(
                renpy.displayable(image_name + "_dream"),
                alpha=dream_alpha
            )
        )

        return d, 0.1

    def dream_char(image_name, pos=None, z=10, transition=dissolve):
        if pos is None:
            pos = []

        low_dream_level=3

        if hero.aspect >= low_dream_level:
            renpy.show(
                image_name,
                tag=image_name.split()[0] + "_shadow",
                at_list=pos + [dream_shadow],
                zorder=z - 1
            )

        renpy.show(
            image_name,
            at_list=pos,
            zorder=z
        )

        renpy.transition(transition)

    def hide_dream_char(image_name, transition=dissolve):
        # Получаем тег персонажа (первое слово в названии)
        tag_name = image_name.split()[0]
        
        # Скрываем тень персонажа
        renpy.hide(tag_name + "_shadow")
        
        # Скрываем самого персонажа
        renpy.hide(tag_name)
        
        # Применяем эффект перехода
        renpy.transition(transition)

    dream_active = True

    # Обработка текста с эффектом сна
    def dreamify(text):
        if hero_selected:
            parts = re.split(r'(\{.*?\})', text)
            result = []
            chance = (hero.aspect - dream_text_min_limit) * 0.1

            for part in parts:
                if part.startswith("{") and part.endswith("}"):
                    result.append(part)
                    continue

                transformed = []

                for char in part:
                    if char in greek_map and random.random() < chance:
                        transformed.append(
                            "{color=#9b59ff}{i}" +
                            "{shader=jitter:u__jitter=1.0,1.0}" +
                            greek_map[char] +
                            "{/shader}" +
                            "{/i}{/color}"
                        )
                    else:
                        transformed.append(char)

                result.append("".join(transformed))

            return "".join(result)
        else:
            return text

    # Вывод текста с эффектами сна
    old_say = renpy.say
    def dream_say(who, what, *args, **kwargs):
        if dream_active:
            what = dreamify(what)

        return old_say(who, what, *args, **kwargs)
    renpy.say = dream_say
