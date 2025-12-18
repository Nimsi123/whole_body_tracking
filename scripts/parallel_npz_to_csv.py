import numpy as np
import glob
import shutil
import os

motion_dir = "/home/nima/holosoma/src/holosoma_retargeting/demo_results_parallel/g1/robot_only/tt4d_mixtape/*.npz"
# motion_dir = "/home/nima/holosoma/src/holosoma_retargeting/demo_results_parallel/g1/robot_only/motive_gameplay/*.npz"

save_dir = "/home/nima/whole_body_tracking/csvs"
if os.path.exists(save_dir):
    shutil.rmtree(save_dir)
os.makedirs(save_dir)

for file_path in glob.glob(motion_dir):
    clip_name = file_path.split("/")[-1][:-4]
    save_path = f"{save_dir}/{clip_name}.csv"
    np.savetxt(save_path, np.load(file_path)["qpos"], delimiter=",")