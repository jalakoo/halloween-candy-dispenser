'''
Manage text-to-speech functions
'''

# TODO: Import text-to-speech library


class Speech:

    def __init__(self):
        # Any necessary set up here
        print("Speech class initialized.")

    def whisper(self, words):
        # For lower volume, slower speech
        # TODO: Code for executing whisper
        return "Speech: whispering {}".format(words)

    def say(self, words):
        # For higher volume, faster speech
        # TODO: Code for executing speech
        return "Speech: saying {}".format(words)
