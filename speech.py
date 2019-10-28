import simpleaudio as sa
import os


class Speech:
    def __init__(self, filePath, *audioFiles):
        # we are going to load all the files into player objects
        self.filePath = filePath
        self._players = {}
        for file in list(audioFiles):
            self._players[file] = sa.WaveObject.from_wave_file(
                os.path.join(filePath, file))
        self._last_audio = None

    def _get(self, filename):
        if filename in self._players.keys():
            ply = self._players[filename]
        else:
            ply = self.load(filename)
        return ply

    def load(self, filename):
        self._players[filename] = sa.WaveObject.from_wave_file(
            os.path.join(self.filePath, filename))
        return self._players[filename]

    def play(self, filename):
        if self._last_audio is not None:
            self._last_audio.stop()
        self._last_audio = self._get(filename).play()

    def play_to_end(self, filename):
        if self._last_audio is not None:
            self._last_audio.stop()
        self._get(filename).play().wait_done()
        self._last_audio = None

    def complete_then_play(self, filename):
        self.wait_done()
        self._last_audio = self._get(filename).play()

    def wait_done(self):
        if self._last_audio is not None:
            self._last_audio.wait_done()


def play_audiofile(filename):
    filePath = os.path.join(os.getcwd(), 'bin', 'audio', filename)
    wave_obj = sa.WaveObject.from_wave_file(filePath)
    play_obj = wave_obj.play()
    play_obj.wait_done()
