# Основное меню
screen main_menu():
    tag menu

    # Добавление вашей картинки на фон
    add "images/bg/_main_menu.png" xsize 1920 ysize 1080

    vbox:
        xpos 0.06
        ypos 0.4
        style_prefix "navigation"
        spacing 15

        # Заменяем сложную проверку на простую логику.
        if renpy.newest_slot(r"^\d.+"):
            textbutton _("Продолжить") action Continue(confirm=False)
        if renpy.list_saved_games(fast=True):
            textbutton _("Новая игра") action Confirm(
                _("Вы уверены? Это действие безвозвратно удалит ВСЕ текущие сохранения."),
                yes=[Function(delete_all_saves), Start()]
            )
        else:
            textbutton _("Новая игра") action Start()
        if debug and renpy.list_saved_games(fast=True):
            textbutton _("Загрузить") action ShowMenu("load")
        textbutton _("Настройки") action ShowMenu("preferences")
        textbutton _("Выход") action Quit(confirm=not main_menu)

    fixed:
        style_prefix "main_menu"

# Настройки
screen preferences():
    tag menu

    vbox:
        xpos 0.3
        ypos 0.8
        style_prefix "navigation"
        spacing 15

        textbutton _("Сохранить") action Return()

    vbox:
        xpos 0.3
        ypos 0.2
        spacing 15

        style_prefix "radio"
        label _("Язык")
        textbutton "Русский" action Language(None)
        textbutton "English" action Language("english")

    vbox:
        xpos 0.3
        ypos 0.5
        spacing 15
        
        if config.has_music:
            label _("Громкость музыки")
            hbox:
                bar value Preference("music volume")

        if config.has_sound:
            label _("Громкость звуков")
            hbox:
                bar value Preference("sound volume")

        if config.has_music or config.has_sound or config.has_voice:
            null height gui.pref_spacing

            textbutton _("Без звука"):
                action Preference("all mute", "toggle")
                style "mute_all_button"