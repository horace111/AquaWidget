import pyglet
import threading

def quick_play(fp):
    sound = pyglet.media.load(fp)
    player = sound.play()
    player.volume = 0.2
    return player

if __name__ == '__main__':
    quick_play('D:\\python_works\\obs\\大喜.flac')