import simpleaudio as sa
import os


class Speech:
    def __init__(self, filePath, *audioFiles):
        # we are going to load all the files into player objects
        self.filePath = filePath
        self._players = {}
        for file in list(audioFiles):
            self._players[file] = sa.WaveObject.from_wave_file(so.path.join(filePath,filename)
            self._last_audio = self._players[file]

    def load(filename):
            self._players[filename] = sa.WaveObject.from_wave_file(so.path.join(filePath,filename)
            return self._players[filename]

    def play(filename):

        self._last_audio.stop()
        if filename in self._players.keys():
            ply = self._players[filename]
        else:
            ply = self.load(filename)
        ply.play()
        self._last_audio = ply

    def compleate_then_play(filename):
        self._last_audio.wait_done()
        if filename in self._players.keys():
            ply = self._players[filename]
        else:
            ply = self.load(filename)
        ply.play()
        self._last_audio = ply


    def wait_done(filename):
        if filename in self._players.keys():
            self._players[filename].wait_done()
        else:
            load(filename).wait_done()

    def play_to_end(filename):
        if filename in self._players.keys():
            ply = self._players[filename]
        else:
            ply = self.load(filename)
        ply.play()
        self._last_audio = ply
        ply.wait_done()


def play_audiofile(filename):
    filePath = os.path.join(os.getcwd(), 'bin', 'audio', filename)
    wave_obj = sa.WaveObject.from_wave_file(filePath)
    play_obj = wave_obj.play()
    play_obj.wait_done()
