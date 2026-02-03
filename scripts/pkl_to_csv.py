"""Convert GMR's .pkl motion files to CSV format compatible with csv_to_npz.py

GMR pkl format:
    - fps: frame rate
    - root_pos: (frames, 3) - base position
    - root_rot: (frames, 4) - base rotation in xyzw format  
    - dof_pos: (frames, dof) - joint positions

CSV output format (same as Unitree's convention):
    - Columns: base_pos_x, base_pos_y, base_pos_z, base_rot_x, base_rot_y, base_rot_z, base_rot_w, dof_pos...

Usage:
    python pkl_to_csv.py --input_file motion.pkl --output_file motion.csv
    
    # Or batch convert all pkl files:
    python pkl_to_csv.py --input_dir /path/to/pkl_dir --output_dir /path/to/csv_dir
"""

import argparse
import pickle
import numpy as np
import os
from pathlib import Path


def convert_pkl_to_csv(pkl_path: str, csv_path: str) -> dict:
    """Convert a single GMR pkl file to CSV format.
    
    Args:
        pkl_path: Path to input .pkl file
        csv_path: Path to output .csv file
        
    Returns:
        dict with metadata (fps, num_frames)
    """
    with open(pkl_path, "rb") as f:
        motion_data = pickle.load(f)
    
    fps = motion_data["fps"]
    root_pos = motion_data["root_pos"]  # (frames, 3)
    root_rot = motion_data["root_rot"]  # (frames, 4) in xyzw format (from GMR)
    dof_pos = motion_data["dof_pos"]    # (frames, dof)
    
    num_frames = root_pos.shape[0]
    
    # IMPORTANT: Convert quaternion from xyzw (GMR output) to wxyz (Isaac Lab expected)
    # GMR saves as xyzw: [x, y, z, w] at indices [0, 1, 2, 3]
    # Isaac Lab expects wxyz: [w, x, y, z]
    # So we reorder: [3, 0, 1, 2] -> [w, x, y, z]
    root_rot_wxyz = root_rot[:, [3, 0, 1, 2]]
    
    # Concatenate: [base_pos(3), base_rot(4 in wxyz), dof_pos(...)]
    motion_csv = np.concatenate([root_pos, root_rot_wxyz, dof_pos], axis=1)
    
    # Save to CSV (no header, comma-separated)
    np.savetxt(csv_path, motion_csv, delimiter=",")
    
    return {
        "fps": fps,
        "num_frames": num_frames,
        "num_dofs": dof_pos.shape[1]
    }


def batch_convert(input_dir: str, output_dir: str) -> None:
    """Convert all .pkl files in a directory to CSV format.
    
    Args:
        input_dir: Directory containing .pkl files
        output_dir: Directory to save .csv files
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    pkl_files = list(input_path.glob("*.pkl"))
    print(f"Found {len(pkl_files)} pkl files in {input_dir}")
    
    for pkl_file in pkl_files:
        csv_filename = pkl_file.stem + ".csv"
        csv_path = output_path / csv_filename
        
        try:
            metadata = convert_pkl_to_csv(str(pkl_file), str(csv_path))
            print(f"✓ {pkl_file.name} -> {csv_filename} "
                  f"(fps={metadata['fps']}, frames={metadata['num_frames']}, dofs={metadata['num_dofs']})")
        except Exception as e:
            print(f"✗ {pkl_file.name}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert GMR pkl motion files to CSV format for BeyondMimic"
    )
    parser.add_argument(
        "--input_file", 
        type=str, 
        help="Path to input .pkl file (for single file conversion)"
    )
    parser.add_argument(
        "--output_file", 
        type=str, 
        help="Path to output .csv file (for single file conversion)"
    )
    parser.add_argument(
        "--input_dir", 
        type=str, 
        help="Directory containing .pkl files (for batch conversion)"
    )
    parser.add_argument(
        "--output_dir", 
        type=str, 
        help="Directory to save .csv files (for batch conversion)"
    )
    
    args = parser.parse_args()
    
    # Single file conversion
    if args.input_file:
        if not args.output_file:
            # Default: same name with .csv extension
            args.output_file = str(Path(args.input_file).with_suffix(".csv"))
        
        metadata = convert_pkl_to_csv(args.input_file, args.output_file)
        print(f"Converted {args.input_file} -> {args.output_file}")
        print(f"  FPS: {metadata['fps']}, Frames: {metadata['num_frames']}, DOFs: {metadata['num_dofs']}")
    
    # Batch conversion
    elif args.input_dir:
        if not args.output_dir:
            raise ValueError("--output_dir required for batch conversion")
        batch_convert(args.input_dir, args.output_dir)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

