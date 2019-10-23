'''
Manage camera + computer vision
'''

import time
import edgeiq


class Vision:
    # Class that uses both an object detection and a tracker

    def __init__(self):
        # Any setup here
        print("Vision class initialized")

    def start(self):
        # This is code from the person-counter app
        # TODO rework this to use a callback, observer-pattern, or generator
        obj_detect = edgeiq.ObjectDetection("alwaysai/mobilenet_ssd")
        obj_detect.load(engine=edgeiq.Engine.DNN_OPENVINO)

        print("Engine: {}".format(obj_detect.engine))
        print("Accelerator: {}\n".format(obj_detect.accelerator))
        print("Model:\n{}\n".format(obj_detect.model_id))

        centroid_tracker = edgeiq.CentroidTracker(
            deregister_frames=20, max_distance=50)
        fps = edgeiq.FPS()

        # Object to store time info for detected people
        allPeople = {}

        try:

            with edgeiq.WebcamVideoStream(cam=0) as video_stream, \
                    edgeiq.Streamer() as streamer:
                # Allow Webcam to warm up
                time.sleep(2.0)
                fps.start()

                # Loop detection and centroid tracker
                while True:
                    frame = video_stream.read()
                    results = obj_detect.detect_objects(
                        frame, confidence_level=.5)

                    # Ignore detections of anything other than people
                    filter = edgeiq.filter_predictions_by_label(
                        results.predictions, ['person'])

                    # Adding info for streamer display
                    text = ["Model: {}".format(obj_detect.model_id)]
                    text.append(
                        "Inference time: {:1.3f} s".format(results.duration))
                    text.append("People currently detected:")

                    objects = centroid_tracker.update(filter)

                    # Store active predictions for just this loop
                    predictions = []
                    # Store the active object ids for just this loop
                    active_ids = []

                    if len(objects.items()) == 0:
                        # No people detected
                        text.append("-- NONE")

                    for (object_id, prediction) in objects.items():
                        seenTime = traffic_manager.timeSeenFor(
                            object_id, allPeople)
                        # Correct id displayed for start of array at index 0
                        actualPersonNumber = object_id + 1

                        # Display general data on person seen
                        new_label = "-- Person {i} | {t} sec".format(
                            i=actualPersonNumber, t=seenTime)
                        active_ids.append(object_id)
                        prediction.label = new_label
                        text.append(new_label)
                        predictions.append(prediction)

                    # Update output streamer
                    frame = edgeiq.markup_image(frame, predictions)
                    streamer.send_data(frame, text)
                    fps.update()

                    if streamer.check_exit():
                        break

        finally:
            fps.stop()
            print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
            print("approx. FPS: {:.2f}".format(fps.compute_fps()))
            print("Program Ending")
