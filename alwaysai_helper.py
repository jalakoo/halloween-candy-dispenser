import time
import edgeiq
import os
import json

'''
full config dictionary:
{
    "model_name":"",                            #alwaysAI model id - Only required param
    "video_mode": "camera",              #camera OR file
    "filter_labels:[],                          #Filter results by matching labels
    "enable_streamer":true,              #Use the debug streamer
    "enable_logs":true,                          #Print simple logs to console
    "object_detection_period":30,               #Frames to skip between detection
    "object_detect_confidence":50,              #Percent confidence filter
    "centroid_deregister_frames":20,            #Frames before object lost
    "centroid_max_distance":50                  #Distance between centroids 1 object
}
'''
MODEL_NAME = 'model_name'
VIDEO_MODE = 'video_mode'
VIDEO_CAMERA_ID = 'video_camera_id'
VIDEO_FILEPATH = 'video_filepath'
FILTER_LABELS = 'filter_labels'
ENABLE_STREAMER = 'enable_streamer'
ENABLE_LOGS = 'enable_logs'
OBJ_DETECTION_PERIOD = 'object_detection_period'
OBJ_DETCTION_CONFIDENCE = 'object_detection_confidence'
CENTROID_FRAMES = 'centroid_deregister_frames'
CENTROID_MAX = 'centroid_max_distance'
'''
full components dictionary:
{
    "fps": f,
    "object_detector": o,
    "streamer": s,
    "tracker": t,
    "video_stream": v
}
'''
FPS = "fps"
OBJECT_DETECTOR = "object_detector"
STREAMER = "streamer"
TRACKER = "tracker"
VIDEO_STREAM = "video_stream"


def loadJSON(filepath):
    if os.path.exists(filepath) == False:
        raise Exception('File at {} does not exist'.format(filepath))
    with open(filepath) as data:
        return json.load(data)


def is_accelerator_available():
    if edgeiq.find_usb_device(id_vendor=edgeiq.constants.NCS1_VID, id_product=edgeiq.constants.NCS1_PID) == True:
        return True
    if edgeiq.find_usb_device(edgeiq.constants.NCS1_VID, edgeiq.constants.NCS1_PID2) == True:
        return True
    if edgeiq.find_usb_device(edgeiq.constants.NCS2_VID, edgeiq.constants.NCS2_PID) == True:
        return True
    return False


def object_detector_from(config):
    model = config[MODEL_NAME]
    return object_detector(model)


def object_detector(model):
    # print("alwaysai_helper.py: object_detector")
    if model is None:
        raise Exception(
            "alwaysai_helper.py: object_detector: model name parameter not found")
    od = edgeiq.ObjectDetection(model)
    engine = edgeiq.Engine.DNN
    if is_accelerator_available() == True:
        engine = edgeiq.Engine.DNN_OPENVINO
    od.load(engine)
    return od


def _video_stream_from(config):
    mode = config[VIDEO_MODE]
    # TODO: Lowercasing?
    if mode == "file":
        filepath = config[VIDEO_MODE]
        return _video_file_stream(filepath)
    camera_id = config[VIDEO_CAMERA_ID]
    return _video_camera_stream(camera_id)


def _video_file_stream(filepath):
    if filepath is None:
        raise Exception(
            "alwaysai_helper.py: video_file_stream: filepath not provided")
    return edgeiq.FileVideoStream(filepath)


def _video_camera_stream(camera_id):
    if camera_id is None:
        # Default cam index
        camera_id = 0
    video_stream = edgeiq.WebcamVideoStream(cam=camera_id)
    time.sleep(2.0)
    return video_stream


def _streamer_from(config):
    # print("alwaysai_helper.py: _streamer_from")
    should_enable = config.get(ENABLE_STREAMER, True)
    if should_enable == True:
        return edgeiq.Streamer()
    return None


def _tracker_from(config):
    # TODO: Switch between centroid and ...
    return _centroid_tracker_from(config)


def _centroid_tracker_from(config):
    # print("alwaysai_helper.py: _centroid_tracker")
    frames = config.get(CENTROID_FRAMES, 20)
    distance = config.get(CENTROID_MAX, 50)
    return edgeiq.CentroidTracker(
        deregister_frames=frames, max_distance=distance)


def _filtered_predictions_from(config, obj_detect, tracker, frame):
    # print("alwaysai_helper.py: _filtered_predictions")
    confidence = config.get(OBJ_DETCTION_CONFIDENCE, .5)
    results = obj_detect.detect_objects(
        frame, confidence_level=confidence)
    #  Why is 'filter' still resulting in a lint error
    filter = edgeiq.filter_predictions_by_label(
        results.predictions, config.get(FILTER_LABELS, []))
    filtered_results = tracker.update(filter)
    return filtered_results


def get_components(config):
    # print("alwaysai_helper.py: get_components")
    fps = edgeiq.FPS()
    fps.start()
    obj_detector = object_detector_from(config)
    streamer = _streamer_from(config)
    tracker = _tracker_from(config)
    video_stream = _video_stream_from(config)
    return {
        FPS: fps,
        OBJECT_DETECTOR: obj_detector,
        STREAMER: streamer,
        TRACKER: tracker,
        VIDEO_STREAM: video_stream
    }


def start_tracking_loop(config, components):
    # print("alwaysai_helper.py: start_tracking_loop")
    video_stream = components[VIDEO_STREAM]
    obj_detector = components[OBJECT_DETECTOR]
    tracker = components[TRACKER]
    if video_stream is None:
        raise Exception(
            "alwaysai_helper.py: start_tracking_loop: video_stream missing from components")
    if obj_detector is None:
        raise Exception(
            "alwaysai_helper.py: start_tracking_loop: object_detector missing from components")
    if tracker is None:
        raise Exception(
            "alwaysai_helper.py: start_tracking_loop: tracker missing from components")
    print("alwaysai_helper.py: start_tracking_loop: about to read frame from {}".format(
        video_stream))
    frame = video_stream.read()
    # print("alwaysai_helper.py: start_tracking_loop: about get filtered predictions...")
    predictions = _filtered_predictions_from(
        config, obj_detector, tracker, frame)
    return predictions


def end_tracking_loop(components, predictions, text):
    # print("alwaysai_helper.py: end_tracking_loop")
    fps = components[FPS]
    streamer = components[STREAMER]
    video_stream = components[VIDEO_STREAM]
    if fps is None:
        raise Exception(
            "alwaysai_helper.py: end_tracking_loop: fps missing from components")
    if streamer is None:
        raise Exception(
            "alwaysai_helper.py: end_tracking_loop: streamer missing from components")
    if video_stream is None:
        raise Exception(
            "alwaysai_helper.py: end_tracking_loop: video_stream missing from components")
    frame = video_stream.read()
    edgeiq.markup_image(frame, predictions)
    streamer.send_data(frame, text)
    fps.update()


def should_exit(components):
    streamer = components[STREAMER]
    if streamer is None:
        print("alwaysai_helper.py: shoud_exit: No streamer found")
        return False
    if streamer.check_exit():
        return True
    return False


def stop_predictions(components):
    # print("alwaysai_helper.py: stop_predictions")
    fps = components[FPS]
    fps.stop()
