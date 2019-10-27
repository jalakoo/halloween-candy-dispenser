"""
Primary run loop and logic
"""

import alwaysai_helper as aai
import motor as m
import speech

CLOSE_THRESHOLD = 50000
SEEN_FAR_IDS = {}
SEEN_NEAR_IDS = {}
AUDIO_PLAYER = speech.Speech(os.path.join(os.getcwd(), 'bin', 'audio'),"vomit_candy.wav", "come_closer.wav")


def main():
    global SEEN_FAR_IDS
    global SEEN_NEAR_IDS
    global AUDIO_PLAYER

    # Load configuration set in alwaysai.app.json so we don't have to
    #  edit code to redeploy with every change
    config = aai.loadJSON('alwaysai.app.json')['tracker_1']

    # Components contains references to aai element such as the
    #  object tracker, centroid tracker, streamer, fps, etc.
    components = aai.get_components(config)

    try:
        # print("app.py: main: try block started")

        # `with` needed to start video stream and streamer
        with components[aai.VIDEO_STREAM] as _, \
                components[aai.STREAMER] as _:
            while True:
                # print("app.py: main: top of while loop")
                tracks = aai.start_tracking_loop(config, components)
                predictions = []
                if len(tracks.items()) == 0:
                    text = ["Waiting for trick-or-treaters"]
                for (object_id, prediction) in tracks.items():
                    text = ["Found me some peeps!"]
                    # print("app.py: main: bounding box area for prediction: {}".format(prediction.box.area))
                    label = "Person {oid} box area: {area}".format(
                        oid=object_id, area=prediction.box.area)
                    prediction.label = label
                    predictions.append(prediction)
                    if is_someone_new_close(object_id, prediction):
                        text.append("Person {} is close".format(object_id))
                        SEEN_NEAR_IDS[object_id] = True
                        dispense_candy()
                    elif is_someone_new_far(object_id, prediction):
                        text.append("Person {} is far".format(object_id))
                        whisper()
                        SEEN_FAR_IDS[object_id] = True

                aai.end_tracking_loop(
                    components, predictions, text)
                if aai.should_exit(components):
                    break

    finally:
        aai.stop_predictions(components)


def is_someone_new_far(object_id, prediction):
    global SEEN_FAR_IDS
    if object_id in SEEN_FAR_IDS:
        return False
    area = prediction.box.area
    if area >= CLOSE_THRESHOLD:
        return False
    return True


def is_someone_new_close(object_id, prediction):
    global SEEN_NEAR_IDS
    if object_id in SEEN_NEAR_IDS:
        return False
    area = prediction.box.area
    if area < CLOSE_THRESHOLD:
        return False
    return True


def dispense_candy():
    print("app.py: dispense_candy")
    # TODO: Start regurgitation sound
    # TODO: Turn motor to drop one candy
    # TODO: Say quirky thankyou
    AUDIO_PLAYER.play("vomit_candy.wav")
    return ""


def whisper():
    print("app.py: whisper")
    # TODO: randomize option
    AUDIO_PLAYER.play("come_closer.wav")
    return ""


if __name__ == "__main__":
    main()
