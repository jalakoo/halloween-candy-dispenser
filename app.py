"""
Primary run loop and logic
"""

import vision as v
import speech as s
import motor as m
import motion as md


def main():
    # Setup all modules
    vision = v.Vision()
    speech = s.Speech()
    motor = m.Motor()
    motion_detector = md.Motion_Detector()

    # TODO: Start a loop or setup callbacks for feedback from the various sensors


if __name__ == "__main__":
    main()
