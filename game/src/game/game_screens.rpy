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
        # textbutton _("Об игре") action ShowMenu("about")
        textbutton _("Выход") action Quit(confirm=not main_menu)

    fixed:
        style_prefix "main_menu"
