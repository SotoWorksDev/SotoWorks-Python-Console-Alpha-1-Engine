# src/audio.py

import pygame as pg

def play_sound(path, volume=0.7):
    snd = pg.mixer.Sound(path)
    snd.set_volume(volume)
    snd.play()

def play_music(path, volume=0.7):
    pg.mixer.music.load(path)
    pg.mixer.music.set_volume(volume)
    pg.mixer.music.play(-1)
