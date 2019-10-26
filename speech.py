from playsound import playsound
import os


class Speech:

    @staticmethod
    def come_here():
        # "Hey, you! Come here."
        playsound(os.path.join(os.getcwd(), 'bin', 'audio', 'come_here.wav'))

    @staticmethod
    def i_can_see_you():
        # "I can see you"
        playsound(os.path.join(os.getcwd(), 'bin', 'audio', 'i_can_see_you.wav'))

    @staticmethod
    def come_closer():
        # "Come over here! Come closer..."
        playsound(os.path.join(os.getcwd(), 'bin', 'audio', 'come_closer.wav'))

    @staticmethod
    def something_for_you():
        # "Here, I have something for you..."
        playsound(os.path.join(os.getcwd(), 'bin', 'audio', 'i_have_something_for_you.wav'))

    @staticmethod
    def vomit():
        # Vomit sound when candy is dispensed
        playsound(os.path.join(os.getcwd(), 'bin', 'audio', 'vomit_candy.wav'))

    @staticmethod
    def happy_halloween():
        # "Happy Halloween!"
        playsound(os.path.join(os.getcwd(), 'bin', 'audio', 'happy_halloween.wav'))

    @staticmethod
    def happy_halloween_laugh():
        # "Happy Halloween! Muahahaha"
        playsound(os.path.join(os.getcwd(), 'bin', 'audio', 'laugh.wav'))


# For testing purposes. Arranged in proper order.
Speech.come_here()
Speech.i_can_see_you()
Speech.come_closer()
Speech.something_for_you()
Speech.vomit()
Speech.happy_halloween()
Speech.happy_halloween_laugh() # Can be swapped for the one above it if desired