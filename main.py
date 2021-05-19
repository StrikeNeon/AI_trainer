import cv2
from pose_estimation import pose_tracker

# TODO pose estimation module
# TODO TTS module
# TODO pose classification module
# TODO excertion calculator module
# TODO main file - video capture and processing

# NOTE order of business - pose estimation first, 
# make a simple test file using downloaded videos
# while ai pose classification is being developed use switched functions

# NOTE I guess I can unify the excercises somewhat
# by counting the distance between
# key points, like wrist to sholder for curls, chest to wrist for pushups etc


cap = cv2.VideoCapture('jerma_walking.mp4')
p_tracker = pose_tracker(debug_draw=True)
try:
    while cap.isOpened():
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (640, 480))

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        pose = p_tracker.find_poses(resized_frame)
        if pose:
            hand_data = p_tracker.get_landmark_data(resized_frame, pose)
            frame = p_tracker.draw_debug_landmarks(resized_frame, pose)
        cv2.imshow('frame', resized_frame)
        if cv2.waitKey(1) == ord('q'):
            break
except cv2.error:
    print("end")
finally:
    cap.release()
    cv2.destroyAllWindows()
