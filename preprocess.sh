cd scripts

# data was pulled from the 
# /home/nima/holosoma/src/holosoma_retargeting/demo_results
# folder
# the stuff from this folder is computed with the first step in holosoma retargeting


# python csv_to_npz.py --input_file /home/nima/whole_body_tracking/artifacts/motive_gameplay_ttg_test_1:v0/motion.csv --input_fps 30 --output_name motion --output_fps 50 --headless

# python replay_npz.py --registry_name=ianc-uc-berkeley-org/wandb-registry-motions/motion