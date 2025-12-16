import numpy as np

path = "/home/nima/whole_body_tracking/npzs/smplh_ttg_test_1.npz"
save_path = "/home/nima/whole_body_tracking/csvs/smplh_ttg_test_1.csv"
np.savetxt(save_path, np.load(path)["qpos"], delimiter=",")