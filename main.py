import cv2
from pose_estimation import pose_tracker
from TTS_speaker import voice_constructor

# TODO pose classification module
# TODO physical excertion calculator module
# TODO main file - video capture and processing

# NOTE order of business - pose estimation first, 
# make a simple test file using downloaded videos
# while ai pose classification is being developed use switched functions

# NOTE I guess I can unify the excercises somewhat
# by counting the distance between
# key points, like wrist to sholder for curls, chest to wrist for pushups etc


def main():
    cam_width, cam_height = 640, 480

    cap = cv2.VideoCapture(0)
    cap.set(3, cam_width), cap.set(4, cam_height)
    # cap = cv2.VideoCapture('jerma_walking.mp4')
    p_tracker = pose_tracker(debug_draw=True)
    voice = voice_constructor()
    found = False
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            pose = p_tracker.find_poses(frame)
            if pose:
                if not found:
                    voice.say_phrase("found you")
                    found = True
                pose_data = p_tracker.get_landmark_data(frame, pose)
                frame = p_tracker.draw_debug_landmarks(frame, pose)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        return(0)
    except cv2.error:
        print("video interrupted")
        cap.release()
        cv2.destroyAllWindows()
        return(1)

main()