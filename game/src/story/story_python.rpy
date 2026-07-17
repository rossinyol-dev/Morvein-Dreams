define slow_dissolve = Dissolve(4.5)

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
    dream_text_min_limit = 6
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

    def start_dream_effect():
        pause_music()
        renpy.sound.play("audio/fx/horror_bell.mp3")
        renpy.music.play(
            "audio/dream_theme.mp3",
            fadein=2.0
        )
        renpy.show("black", layer="background")
        renpy.layer_at_list([slow_shaking], layer="master")

    def start_dream_effect_without_music():
        renpy.sound.play("audio/fx/horror_bell.mp3")
        renpy.show("black", layer="background")
        renpy.layer_at_list([slow_shaking], layer="master")

    def stop_dream_effect():
        renpy.music.stop(fadeout=2.0)
        resume_music()
        renpy.layer_at_list([], layer="master")

    def stop_dream_effect_without_music():
        renpy.layer_at_list([], layer="master")

    def hard_fade(scene_name, delay=3.0, texts = None, show_gui=True, dream=True):
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

        if dream:
            renpy.show(
                scene_name,
                what=DynamicDisplayable(dream_scene_dynamic, scene_name),
                layer="master",
                at_list=[fade_in_from_black(delay)]
            )
        else:
            renpy.show(scene_name, layer="master", at_list=[fade_in_from_black(delay)])
        renpy.pause(delay, hard=True)

        if show_gui:
            renpy.show_screen("gui")
        
    def dream_scene_dynamic(st, at, image_name):
        global dream_alpha

        if globals().get("hero_selected", False):
            dream_alpha = max(0.0, min(1.0, (hero.aspect - 5) * 0.25))
        else:
            dream_alpha = 0.0

        if dream_alpha <= 0.0:
            return renpy.displayable(image_name), 0.1

        base = renpy.displayable(image_name)
        purple_alpha = dream_alpha * 0.55
        red_alpha = dream_alpha * 0.25
        amber_alpha = dream_alpha * 0.12

        d = Composite(
            (1920, 1080),
            (0, 0), renpy.displayable(image_name),
            (0, 0), Transform(
                renpy.displayable(image_name + "_dream"),
                alpha=dream_alpha
            )
        )
        return d, 0.1

        fade_to_black()

    def dream_char(image_name, pos=None, z=10, transition=dissolve):
        if pos is None:
            pos = []

        low_dream_level=4

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
    
    def fade_to_black(fade_time=3.0, pause_time=5.0, hide_screen=None):
        """
        Полностью рабочая функция. Принимает аргументы, но использует 
        твой стабильный статичный трансформ.
        """
        # Скрываем интерфейс диалогов
        renpy.with_statement(None)
        renpy.hide_screen("say")
        _window_hide(None)
        
        # Показываем черный цвет, используя твой рабочий трансформ smooth_fade_out
        renpy.show("black_screen", what=renpy.display.image.Solid("#000"), layer="master", at_list=[smooth_fade_out])
        
        # Скрываем кровь (или другой экран), если передано имя
        if hide_screen is not None:
            renpy.hide_screen(hide_screen)
            renpy.with_statement(dissolve)
        else:
            renpy.with_statement(None)
            
        # Считаем общую паузу на основе переданных ТОБОЙ чисел
        total_pause = fade_time + pause_time
        renpy.pause(total_pause, hard=True)

    def audio_duration(track, fallback=3.8):
        try:
            duration = renpy.music.get_duration(track)
            if duration:
                return duration
        except Exception:
            pass

        return fallback

    def start_act(title, subtitle, act_num, scene):
        act_start_track = "audio/act_start.mp3"
        act_start_duration = audio_duration(act_start_track)

        renpy.music.play(act_start_track, channel="music", loop=False)

        renpy.hide_screen("gui")
        renpy.hide_screen("say")
        renpy.hide_screen("quick_menu")

        renpy.scene(layer="screens")
        renpy.scene(layer="overlay")
        renpy.scene(layer="master")

        renpy.show("black", layer="master")
        renpy.with_statement(fade)

        renpy.call("show_act_title", title, subtitle, act_start_duration)

        return scene
