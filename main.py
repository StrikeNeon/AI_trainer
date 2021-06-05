import asyncio
import cv2
from pose_estimation import pose_tracker
from lift_computer import compute_bicep_curl
from TTS_speaker import voice_constructor
import threading


# TODO pose classification module
# TODO physical excertion calculator module
# TODO main file - video capture and processing

# NOTE order of business - pose estimation first, 
# make a simple test file using downloaded videos
# while ai pose classification is being developed use switched functions

# NOTE I guess I can unify the excercises somewhat
# by counting the distance between
# key points, like wrist to sholder for curls, chest to wrist for pushups etc


def main(excercise: str, ex_limit: int):
    cam_width, cam_height = 640, 480

    cap = cv2.VideoCapture(0)
    cap.set(3, cam_width), cap.set(4, cam_height)
    # cap = cv2.VideoCapture('jerma_walking.mp4')
    ex_dict = {"curls": compute_bicep_curl, "push-up": None, "bench": None}
    p_tracker = pose_tracker(debug_draw=False)
    voice = voice_constructor()
    voice_thread = threading.Thread(target=voice.loop)
    voice_thread.start()
    found = False
    started = False
    finished = False
    lift_done = False
    lifts = 0
    ex_limit = ex_limit
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            pose = p_tracker.find_poses(frame)
            if pose:
                if not found:
                    voice.engine.say("найден")
                    found = True
                pose_data = p_tracker.get_landmark_data(frame, pose)

                # classifier here, matching scheduled pose to classified and ensuring starting teminal state

                completion, frame = ex_dict[excercise](p_tracker,
                                                       pose_data,
                                                       frame)
                if completion == 0:
                    if not finished:
                        started = True
                        lift_done = False
                    else:
                        lifts = 0
                        lift_done = False
                        finished = False
                        voice.engine.say("погнал")
                if started and completion < 1:
                    print(completion)
                if started and completion == 1:
                    if lift_done:
                        pass
                    else:
                        if lifts+1 == ex_limit:
                            if not finished:
                                finished = True
                                voice.engine.say(f"{ex_limit}")
                                voice.engine.say("закончил")
                            else:
                                pass
                        else:
                            lifts += 1
                            voice.engine.say(f"{lifts}")
                        lift_done = True
            else:
                if found:
                    voice.engine.say("потерян")
                    found = False
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        voice.shutdown = True
        voice.engine.stop()
        voice_thread.join()
        return(0)
    except cv2.error:
        print("video interrupted")
        cap.release()
        cv2.destroyAllWindows()
        voice.shutdown = True
        voice.engine.stop()
        voice_thread.join()
        return(1)


main("curls", 10)
