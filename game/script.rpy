# Флаги истории
default hero_selected = False
default tutorial_shown_flag = False
default inventory_tutorial_blink = False

# Флаги квестов
default beggar_flag_help = False
default agatha_release_flag = False
default agatha_arrested_flag = False
default agatha_runaway_flag = False
default council_help_flag = False
default trillian_seal_found_flag = False
default stefan_saved_flag = False
default order_history_explored_flag = False
default girl_picture_found_flag = False
default singer_saved_flag = False
default hero_saved_by_guard = False
default choir_notes_found_flag = False

# Флаги готовности
default finished_act = False

# Точка входа
label start:
    $ quick_menu = debug and not renpy.variant("web")
    $ _skipping = debug
    $ _game_menu_screen = None
    $ preferences.afm_enable = not debug
    $ preferences.afm_time = 10.0

    play music "audio/main_theme.m4a"

    $ hero = Hero(
        name = "...", 
        full_name = "...", 
        prof = PROF.MONK, 
        state = STATE.HEALTHY, 
        mercy = 0, 
        reason = 0, 
        aspect = 0, 
        control = 0, 
        image = "...",
        portrait = "...",
        color="#000000")

    jump prologue
