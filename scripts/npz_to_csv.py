import numpy as np

path = "/home/nima/whole_body_tracking/pre_formatting_motions/smplh_ttg_test_1.npz"
save_path = "/home/nima/whole_body_tracking/artifacts/motive_gameplay_ttg_test_1:v0/motion.csv"
np.savetxt(save_path, np.load(path)["qpos"], delimiter=",")