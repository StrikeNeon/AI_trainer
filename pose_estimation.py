import math
import mediapipe
from numpy import ndarray, interp
from cv2 import line

class pose_tracker():
    def __init__(self, mode: bool = False, upBody: bool = False, smooth: bool = True,
                 model_complexity: int = 0, debug_draw: bool = False,
                 min_detection_confidence: float = 0.8, min_tracking_confidence: float = 0.5):
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
            pose_data[landmark_id] = [landmark.x, landmark.y,
                                      landmark.z, cx, cy]
        return pose_data

    def draw_debug_landmarks(self, rgb_frame: ndarray, pose: list):

        if self.debug_draw:
            self.debug_draw.draw_landmarks(rgb_frame, pose, self.mp_pose.POSE_CONNECTIONS)
        return rgb_frame

    def draw_joint_group(self, rgb_frame: ndarray, joint_group: list):
        # joint group 0 is x, 1 is y
        # a joint group would be 2 lines
        line(rgb_frame,
             (joint_group[0][0], joint_group[0][1]),
             (joint_group[1][0], joint_group[1][1]),
             (155, 0, 0), 3)
        line(rgb_frame,
             (joint_group[1][0], joint_group[1][1]),
             (joint_group[2][0], joint_group[2][1]),
             (155, 0, 0), 3)

    def format_joint_group(self, joints: list):
        joint_group = [[joint[3], joint[4]] for joint in joints]
        return joint_group

    def get_joint_angles(self, joint_group: list):
        return math.degrees(math.atan2(joint_group[2][1]-joint_group[1][1],
                                       joint_group[2][0]-joint_group[1][0]) -
                            math.atan2(joint_group[0][1]-joint_group[1][1],
                                       joint_group[0][0]-joint_group[1][0]))

    def compute_completion(self, angle: float, l_bound: int, u_bound: int):
        return interp(angle, [u_bound, l_bound], [1.0, 0.0])

    def get_keypoint_distance(self, keypoints: list):
        return math.hypot(keypoints[0][0]-keypoints[1][0],
                          keypoints[0][1]-keypoints[1][1])
