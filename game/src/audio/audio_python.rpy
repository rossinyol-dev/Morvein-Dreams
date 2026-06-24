default saved_music_pos = 0.0
default saved_music_file = None

init python:
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