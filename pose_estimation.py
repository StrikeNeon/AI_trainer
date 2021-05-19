import mediapipe
from numpy import ndarray


class pose_tracker():
    def __init__(self, debug_draw: bool = False, min_detection_confidence: float = 0.7, min_tracking_confidence: float = 0.5):
        self.mp_pose = mediapipe.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=min_detection_confidence,
                                      min_tracking_confidence=min_tracking_confidence)
        if debug_draw:
            self.debug_draw = mediapipe.solutions.drawing_utils
        else:
            self.debug_draw = None

    def find_poses(self, rgb_frame: ndarray):

        result = self.pose.process(rgb_frame)
        if result.pose_landmarks:
            pose = result.pose_landmarks
            return pose

    def get_landmark_data(self, rgb_frame: ndarray, pose: list):

        pose_data = {}
        for landmark_id, landmark in enumerate(pose.landmark):
            height, width, channels = rgb_frame.shape
            cx, cy = int(landmark.x*width), int(landmark.y*height)
            pose_data[landmark_id] = [landmark.x, landmark.y, landmark.z, cx, cy]
        return pose_data

    def draw_debug_landmarks(self, frame: ndarray, pose: list):

        if self.debug_draw:
            self.debug_draw.draw_landmarks(frame, pose, self.mp_pose.POSE_CONNECTIONS)
        return frame
