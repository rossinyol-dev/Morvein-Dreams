define debug = True
define config.menu_include_disabled = debug
define config.rollback_enabled = debug
define config.default_afm_enable = debug
define config.gl_clear_color = "#000"
define gui.main_menu_background = "#000"
define quick_menu = debug and not renpy.variant("web")
default preferences.afm_enable = debug
default preferences.afm_after_click = debug

define config.has_autosave = debug
define config.has_quicksave = debug
define config.autosave_on_choice = debug
define config.autosave_on_quit = debug
define config.autosave_frequency = 200 if debug else None

init python:
    if not debug:
        config.keymap['quick_save'] = []
        config.keymap['quick_load'] = []
define config.default_textshader = "typewriter"

define gui.text_font = "fonts/main/main-regular.otf"
define gui.interface_text_font = "fonts/main/main-regular.otf"
define gui.label_text_font = "fonts/main/main-regular.otf"
define gui.name_text_font = "fonts/main/main-regular.otf"
define gui.text_size = 38
