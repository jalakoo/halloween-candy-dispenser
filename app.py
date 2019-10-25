"""
Primary run loop and logic
"""

import alwaysai_helper as aai
import speech as s
import motor as m
import motion as md


def main():
    # print("app.py: main")
    # Load configuration set in alwaysai.app.json so we don't have to
    #  edit code to redeploy with every change
    config = aai.loadJSON('alwaysai.app.json')['tracker_1']

    # Components contains references to aai element such as the
    #  object tracker, centroid tracker, streamer, fps, etc.
    components = aai.get_components(config)

    anyone = False
    try:
        # print("app.py: main: try block started")
        # With needed to start video stream and streamer
        with components[aai.VIDEO_STREAM] as _, \
                components[aai.STREAMER] as _:
            while True:
                # print("app.py: main: top of while loop")
                tracks = aai.start_tracking_loop(config, components)
                if len(tracks.items()) == 0:
                    anyone = False
                predictions = []
                for (object_id, prediction) in tracks.items():
                    predictions.append(prediction)
                    print('Object: {o}, Prediction: {p}'.format(
                        o=object_id, p=prediction))
                    if anyone == False:
                        if is_someone_new_close(prediction):
                            dispense_candy()
                        elif is_someone_new_far(prediction):
                            whisper()
                    elif is_someone_new_close(prediction):
                        dispense_candy
                    anyone = True

                aai.end_tracking_loop(
                    components, predictions, "Additional Debug Text Here")
                if aai.should_exit(components):
                    break
                # print("app.py: main: end of while loop")

    finally:
        aai.stop_predictions(components)


def is_someone_new_far(prediction):
    # TODO
    return False


def is_someone_new_close(prediction):
    # TODO
    return False


def dispense_candy():
    # TODO: Start regurgitation sound
    # TODO: Turn motor to drop one candy
    # TODO: Say quirky thankyou
    return ""


def whisper():
    # TODO:
    return ""


if __name__ == "__main__":
    main()
