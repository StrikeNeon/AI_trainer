import cv2
from pose_estimation import pose_tracker
from lift_computer import compute_bicep_curl
from TTS_speaker import voice_constructor
import time


# TODO timer calibration module - upper median and lower bands of time
#  elapsed on the excercise

# TODO pose classification module

# TODO physical excertion calculator module

# TODO main file - video capture and processing

# NOTE I guess I can unify the excercises somewhat
# by counting the distance between
# key points, like wrist to sholder for curls, chest to wrist for pushups etc


class TimerError(Exception):
    pass


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def get_running_time(self):
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        return round(elapsed_time, 2)

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        # print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return round(elapsed_time, 2)


def main(excercise: str, ex_limit: int, lift_median: float):
    cam_width, cam_height = 640, 480

    cap = cv2.VideoCapture(0)
    cap.set(3, cam_width), cap.set(4, cam_height)
    # cap = cv2.VideoCapture('jerma_walking.mp4')
    ex_dict = {"curls": compute_bicep_curl, "push-up": None, "bench": None}
    p_tracker = pose_tracker(debug_draw=False)
    voice = voice_constructor()
    found = False
    started = False
    finished = False
    lift_done = False
    lifts = 0
    lift_timer = Timer()
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            pose = p_tracker.find_poses(frame)
            if pose:
                if not found:
                    voice.say_command("найден")
                    found = True
                pose_data = p_tracker.get_landmark_data(frame, pose)

                # classifier here, matching scheduled pose to classified and ensuring valid teminal state

                completion, frame = ex_dict[excercise](p_tracker,
                                                       pose_data,
                                                       frame)
                if completion == 0:
                    if not finished:
                        started = True
                        lift_done = False
                        try:
                            lift_timer.start()
                        except TimerError:
                            pass
                    else:
                        lifts = 0
                        lift_done = False
                        finished = False
                        lift_timer.start()
                        voice.say_command("погнал")
                if started and 0 < completion < 1:
                    print(completion)
                if started and completion == 1:
                    if lift_done or lift_timer.get_running_time() < 1:
                        pass
                    else:
                        if lifts+1 == ex_limit:
                            if not finished:
                                finished = True
                                voice.say_command(f"{ex_limit}")
                                voice.say_command("закончил")
                            else:
                                pass
                        else:
                            lifts += 1
                            voice.say_command(f"{lifts}")
                            print(lifts)
                        lift_done = True
                        time_spent = lift_timer.get_running_time()
                        
                        if time_spent > lift_median+1:
                            voice.say_command(f"быстрее ебаш")
                        elif lift_median+1 > time_spent > lift_median-0.5:
                            voice.say_command(f"ок")
                        elif time_spent < lift_median-0.5:
                            voice.say_command(f"тормозни")
                        stop_time = lift_timer.stop()
                        print(stop_time)
            else:
                if found:
                    voice.say_command("потерян")
                    found = False
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        voice.shutdown = True
        voice.engine.stop()
        return(0)
    except cv2.error:
        print("video interrupted")
        cap.release()
        cv2.destroyAllWindows()
        voice.shutdown = True
        voice.engine.stop()
        return(1)


main("curls", 10, 1.5)
