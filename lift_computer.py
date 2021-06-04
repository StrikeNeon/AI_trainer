
def compute_bicep_curl(p_tracker, pose_data, frame):
    # check which sholder is closer (pose data z value) to determine which angle should be referenced
    try:
        r_arm_group = p_tracker.format_joint_group([pose_data.get(12),
                                                    pose_data.get(14),
                                                    pose_data.get(16)])
        p_tracker.draw_joint_group(frame, r_arm_group)
        r_angle = p_tracker.get_joint_angles(r_arm_group)
        if r_angle < 0:
            r_angle = r_angle*-1
        lift_completion = p_tracker.compute_completion(r_angle,
                                                       40, 150)
        return lift_completion, frame
    except Exception as ex:
        print(ex)
