"""
Primary run loop and logic
"""

import alwaysai_helper as aai
import file_manager as fm
import motor as m
import random
import speech
import os

# Bounding box area threshold to distinguish between
#  a close and far person
# CLOSE_THRESHOLD = 50000
SEEN_FAR_IDS = {}
SEEN_NEAR_IDS = {}
AUDIO_PLAYER = speech.Speech(os.path.join(
    os.getcwd(), 'bin', 'audio'), "vomit_candy.wav", "come_closer.wav")


def main():
    global SEEN_FAR_IDS
    global SEEN_NEAR_IDS
    global AUDIO_PLAYER
    app_settings = fm.loadJSON('alwaysai.app.json')["settings"]
    close_threshold = app_settings.get("close_threshold", 50000)
    # Load configuration set in alwaysai.app.json so we don't have to
    #  edit code to redeploy with every change
    aai_config = fm.loadJSON('alwaysai.app.json')['tracker_1']

    # Components contains references to aai element such as the
    #  object tracker, centroid tracker, streamer, fps, etc.
    components = aai.get_components(aai_config)

    try:
        # print("app.py: main: try block started")

        # `with` needed to start video stream and streamer
        #  TODO: How does this work if we're optionally disabling the streamer?
        with components[aai.VIDEO_STREAM] as _, \
                components[aai.STREAMER] as _:

            while True:
                # print("app.py: main: top of while loop")
                tracks = aai.start_tracking_loop(aai_config, components)
                predictions = []
                candy_to_dispense = 0
                if len(tracks.items()) == 0:
                    text = ["Waiting for trick-or-treaters"]
                for (object_id, prediction) in tracks.items():
                    text = ["Found me some peeps!"]
                    # print("app.py: main: bounding box area for prediction: {}".format(prediction.box.area))
                    label = "Person {oid} box area: {area}".format(
                        oid=object_id, area=prediction.box.area)
                    prediction.label = label
                    predictions.append(prediction)
                    if is_someone_new_close(object_id, prediction, close_threshold):
                        text.append("Person {} is close".format(object_id))
                        SEEN_NEAR_IDS[object_id] = True
                        candy_to_dispense += 1
                        # dispense_candy()
                    elif is_someone_new_far(object_id, prediction, close_threshold):
                        text.append("Person {} is far".format(object_id))
                        whisper()
                        SEEN_FAR_IDS[object_id] = True

                dispense_candy(candy_to_dispense, app_settings)
                aai.end_tracking_loop(
                    components, predictions, text)
                # aai.updateStream(frame, streamer, fps, predictions, text)
                if aai.should_exit(components):
                    break

    finally:
        # fps.stop()
        aai.stop_predictions(components)


def is_someone_new_far(object_id, prediction, close_threshold):
    global SEEN_FAR_IDS
    if object_id in SEEN_FAR_IDS:
        return False
    area = prediction.box.area
    if area >= close_threshold:
        return False
    return True


def is_someone_new_close(object_id, prediction, close_threshold):
    global SEEN_NEAR_IDS
    if object_id in SEEN_NEAR_IDS:
        return False
    area = prediction.box.area
    if area < close_threshold:
        return False
    return True


def dispense_candy(candies_to_dispense, app_settings):
    if candies_to_dispense == 0:
        return ""
    print("app.py: dispense_candy: candies: {}".format(candies_to_dispense))
    if candies_to_dispense > app_settings.get("vomit_threshold", 2):
        AUDIO_PLAYER.complete_then_play("vomiting-01.wav")
        return ""
    for _ in range(candies_to_dispense):
        AUDIO_PLAYER.complete_then_play("vomiting-06.wav")
    # TODO: Call motor to dispense candy
    return ""


def whisper():
    print("app.py: whisper")
    AUDIO_Sounds = ["come_here.wav", "come_closer.wav",
                    "i_can_see_you.wav", "i_have_something_for_you.wav"]
    AUDIO_Random = random.choice(AUDIO_Sounds)
    AUDIO_PLAYER.complete_then_play(AUDIO_Random)
    return ""


if __name__ == "__main__":
    main()
