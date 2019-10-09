import os
import pygame

sounds = {}

menu_music_name = "darkling-by-kevin-macleod.ogg"
bg_music_names = ["chase-pulse-faster-by-kevin-macleod.ogg",
                  "chase-pulse-faster-by-kevin-macleod_1.ogg",
                  "chase-pulse-faster-by-kevin-macleod_2.ogg"]


def play_music(name, volume=0.5):
    try:
        pygame.mixer_music.stop()
        pygame.mixer_music.load(os.path.join("music", name))
        pygame.mixer_music.set_volume(volume)
        pygame.mixer_music.play(-1)
    except pygame.error:
        pass


def play(sound_name, loop=False):
    if sound_name in sounds:
        sounds[sound_name].play(-1 if loop else 0)


def stop(sound_name):
    if sound_name in sounds:
        sounds[sound_name].stop()


def silence(sound_name=None):
    if sound_name is None:
        """silence all sound fx"""
        for key in sounds.keys():
            sounds[key].stop()

    else:
        if sound_name in sounds:
            sounds[sound_name].stop()


def fade_in(sound_name, time_ms, loop=False):
    if sound_name in sounds:
        sounds[sound_name].play(loops=-1 if loop else 0, fade_ms=time_ms)


def fade_out(sound_name, time_ms):
    if sound_name in sounds:
        sounds[sound_name].fadeout(time_ms)


def is_playing(sound_name):
    if sound_name in sounds:
        return True if sounds[sound_name].get_num_channels() > 0 else False


def load_sounds():
    if pygame.mixer:
        for filename in os.listdir(os.fsencode("sounds")):
            full_path = os.path.join("sounds", os.fsdecode(filename))

            if os.path.isfile(full_path):
                name = os.fsdecode(os.path.splitext(filename)[0])

                try:
                    sounds[name] = pygame.mixer.Sound(file=full_path)
                    sounds[name].set_volume(0.5)
                except pygame.error:
                    print("ERROR: unable to load sound ", name)
