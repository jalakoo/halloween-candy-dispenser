"""
Primary run loop and logic
"""

import alwaysai_helper as aai
import motor as m
import speech
import os

# Bounding box area threshold to distinguish between
#  a close and far person
CLOSE_THRESHOLD = 50000
SEEN_FAR_IDS = {}
SEEN_NEAR_IDS = {}
AUDIO_PLAYER = speech.Speech(os.path.join(
    os.getcwd(), 'bin', 'audio'), "vomit_candy.wav", "come_closer.wav")


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
    # object_detector = aai.object_detector_from(config)
    # tracker = aai.tracker_from(config)
    # fps = aai.fps_monitor()

    try:
        # print("app.py: main: try block started")

        # `with` needed to start video stream and streamer
        #  TODO: How does this work if we're optionally disabling the streamer?
        with components[aai.VIDEO_STREAM] as _, \
                components[aai.STREAMER] as _:
            # with aai.video_stream_from(config) as video_stream, \
            #         aai.streamer_from(config) as streamer:

            # fps.start()

            while True:
                # print("app.py: main: top of while loop")
                tracks = aai.start_tracking_loop(config, components)
                # frame = video_stream.read()
                # tracks = aai.filtered_predictions_from(
                #     config, object_detector, tracker, frame)
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
                # aai.updateStream(frame, streamer, fps, predictions, text)
                if aai.should_exit(components):
                    break

    finally:
        # fps.stop()
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
    AUDIO_PLAYER.play("vomit_candy.wav")
    # TODO: Turn motor to drop one candy
    # TODO: Say quirky thankyou
    # AUDO_PLAYER.complete_then_play("thank_you.wav")
    return ""


def whisper():
    print("app.py: whisper")
    # TODO: randomize option
    AUDIO_PLAYER.play("come_closer.wav")
    return ""


if __name__ == "__main__":
    main()
