#!/usr/bin/env python3
"""Migrate existing motion .npz files to include body_names and joint_names.

This script adds the required metadata to motion files created with older versions
of csv_to_npz.py, enabling cross-simulator compatibility (Isaac Lab -> MuJoCo).

Usage:
    python migrate_motion_npz.py --input_dir /path/to/motions
    python migrate_motion_npz.py --input_file /path/to/motion.npz
"""

import argparse
import glob
import numpy as np
import os

# Isaac Lab body names for G1 robot (40 bodies in order)
ISAAC_LAB_BODY_NAMES = [
    "pelvis",
    "imu_in_pelvis",
    "left_hip_pitch_link",
    "pelvis_contour_link",
    "right_hip_pitch_link",
    "waist_yaw_link",
    "left_hip_roll_link",
    "right_hip_roll_link",
    "waist_roll_link",
    "left_hip_yaw_link",
    "right_hip_yaw_link",
    "torso_link",
    "left_knee_link",
    "right_knee_link",
    "head_link",
    "imu_in_torso",
    "left_shoulder_pitch_link",
    "logo_link",
    "mid360_link",
    "right_shoulder_pitch_link",
    "left_ankle_pitch_link",
    "right_ankle_pitch_link",
    "left_shoulder_roll_link",
    "right_shoulder_roll_link",
    "left_ankle_roll_link",
    "right_ankle_roll_link",
    "left_shoulder_yaw_link",
    "right_shoulder_yaw_link",
    "LL_FOOT",
    "LR_FOOT",
    "left_elbow_link",
    "right_elbow_link",
    "left_wrist_roll_link",
    "right_wrist_roll_link",
    "left_wrist_pitch_link",
    "right_wrist_pitch_link",
    "left_wrist_yaw_link",
    "right_wrist_yaw_link",
    "left_rubber_hand",
    "right_racket",
]

# Isaac Lab joint names for G1 robot (29 joints in order)
ISAAC_LAB_JOINT_NAMES = [
    "left_hip_pitch_joint",
    "left_hip_roll_joint",
    "left_hip_yaw_joint",
    "left_knee_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_hip_pitch_joint",
    "right_hip_roll_joint",
    "right_hip_yaw_joint",
    "right_knee_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",
    "waist_yaw_joint",
    "waist_roll_joint",
    "waist_pitch_joint",
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "left_wrist_pitch_joint",
    "left_wrist_yaw_joint",
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
    "right_wrist_pitch_joint",
    "right_wrist_yaw_joint",
]


def migrate_file(filepath: str, dry_run: bool = False) -> bool:
    """Add body_names and joint_names to a motion file if missing.
    
    Returns True if the file was modified.
    """
    data = dict(np.load(filepath))
    modified = False
    
    # Check current state
    has_body_names = "body_names" in data
    has_joint_names = "joint_names" in data
    
    if has_body_names and has_joint_names:
        print(f"  [SKIP] {filepath} - already has body_names and joint_names")
        return False
    
    # Validate shapes match expected Isaac Lab format
    body_count = data["body_pos_w"].shape[1]
    joint_count = data["joint_pos"].shape[1]
    
    if body_count != len(ISAAC_LAB_BODY_NAMES):
        print(f"  [WARN] {filepath} - unexpected body count {body_count} "
              f"(expected {len(ISAAC_LAB_BODY_NAMES)})")
        return False
        
    if joint_count != len(ISAAC_LAB_JOINT_NAMES):
        print(f"  [WARN] {filepath} - unexpected joint count {joint_count} "
              f"(expected {len(ISAAC_LAB_JOINT_NAMES)})")
        return False
    
    # Add missing metadata
    if not has_body_names:
        data["body_names"] = np.array(ISAAC_LAB_BODY_NAMES)
        modified = True
        
    if not has_joint_names:
        data["joint_names"] = np.array(ISAAC_LAB_JOINT_NAMES)
        modified = True
    
    if modified and not dry_run:
        np.savez(filepath, **data)
        print(f"  [OK] {filepath} - added metadata")
    elif modified and dry_run:
        print(f"  [DRY-RUN] {filepath} - would add metadata")
        
    return modified


def main():
    parser = argparse.ArgumentParser(
        description="Migrate motion .npz files to include body_names and joint_names"
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        help="Directory containing motion .npz files to migrate"
    )
    parser.add_argument(
        "--input_file",
        type=str,
        help="Single motion .npz file to migrate"
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Don't actually modify files, just print what would be done"
    )
    args = parser.parse_args()
    
    if not args.input_dir and not args.input_file:
        parser.error("Must specify either --input_dir or --input_file")
    
    files = []
    if args.input_file:
        files.append(args.input_file)
    if args.input_dir:
        files.extend(glob.glob(os.path.join(args.input_dir, "*.npz")))
    
    print(f"Found {len(files)} .npz files to process")
    
    modified_count = 0
    for filepath in sorted(files):
        if migrate_file(filepath, dry_run=args.dry_run):
            modified_count += 1
    
    print(f"\nDone! Modified {modified_count}/{len(files)} files")


if __name__ == "__main__":
    main()
