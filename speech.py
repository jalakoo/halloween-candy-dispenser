import simpleaudio as sa
import os


def play_audiofile(filename):
    filePath = os.path.join(os.getcwd(), 'bin', 'audio', filename)
    wave_obj = sa.WaveObject.from_wave_file(filePath)
    play_obj = wave_obj.play()
    play_obj.wait_done()
