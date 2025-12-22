conda activate beyondmimic

# data was pulled from the 
# /home/nima/holosoma/src/holosoma_retargeting/demo_results
# folder
# the stuff from this folder is computed with the first step in holosoma retargeting

# python scripts/csv_to_npz.py --input_file /home/nima/whole_body_tracking/csvs/smplh_ttg_test_1.csv --input_fps 30 --output_name smplh_ttg_test_1 --output_fps 50 --headless
# python scripts/replay_npz.py --registry_name=ianc-uc-berkeley-org/wandb-registry-motions/smplh_ttg_test_1

# python scripts/csv_to_npz.py --input_file /home/nima/whole_body_tracking/csvs/smplh_ttg_test_1.csv --input_fps 30 --output_name smplh_ttg_test_1 --output_fps 50 --headless
# python scripts/replay_npz.py --registry_name=ianc-uc-berkeley-org/wandb-registry-motions/smplh_ttg_test_1

# python scripts/csv_to_npz.py --input_file /home/nima/whole_body_tracking/csvs/-7lbDSIKUak_232930_233555_0_1_2_2_original.csv --input_fps 30 --output_name -7lbDSIKUak_232930_233555_0_1_2_2_original --output_fps 50 --headless
# python scripts/replay_npz.py --registry_name=ianc-uc-berkeley-org/wandb-registry-motions/-7lbDSIKUak_232930_233555_0_1_2_2_original

# python scripts/csv_to_npz.py --input_file "/home/nima/whole_body_tracking/csvs/Take_2025-09-30_03.21.33_PM_part000_6_2_original.csv" --input_fps 30 --output_name motive_repeated --output_fps 50 --headless
# python scripts/replay_npz.py --registry_name=ianc-uc-berkeley-org/wandb-registry-motions/motive_repeated

# python scripts/csv_to_npz.py --input_file "/home/nima/whole_body_tracking/csvs/Take_2025-09-30_03.38.11_PM_part000_9_2_original.csv" --input_fps 30 --output_name motive_repeated_5 --output_fps 50 --headless
# python scripts/replay_npz.py --registry_name=ianc-uc-berkeley-org/wandb-registry-motions/motive_repeated_5

# python scripts/csv_to_npz.py --input_file "/home/nima/whole_body_tracking/csvs/-7lbDSIKUak_224590_225140_0_5_1_4_3_original.csv" --input_fps 30 --output_name smpl_extreme_2 --output_fps 50 --headless
# python scripts/replay_npz.py --registry_name=ianc-uc-berkeley-org/wandb-registry-motions/smpl_extreme_2


# after SMPL trajectory filtering

# cd /home/nima/holosoma/src/holosoma_retargeting/demo_results_parallel/g1/robot_only
# rm -rf tt4d_mixtape && rsync -av nima@em3.ist.berkeley.edu:/home/nima/holosoma/src/holosoma_retargeting/demo_results_parallel/g1/robot_only/tt4d_mixtape .
# python scripts/parallel_npz_to_csv.py

# # sim2sim did not work
# python scripts/csv_to_npz.py --input_file "/home/nima/whole_body_tracking/csvs/4deOUpU2sis_298361_298931_0_3_0_3_original.csv" --input_fps 30 --output_name smpl_extreme_filtered_0 --output_fps 50 --headless
# python scripts/replay_npz.py --registry_name=ianc-uc-berkeley-org/wandb-registry-motions/smpl_extreme_filtered_0

python scripts/csv_to_npz.py --input_file "/home/nima/whole_body_tracking/csvs/-_2U39bWx-k_43432_44112_1_2_1_1_0_original.csv" --input_fps 30 --output_name smpl_extreme_filtered_1 --output_fps 50 --headless
python scripts/replay_npz.py --registry_name=ianc-uc-berkeley-org/wandb-registry-motions/smpl_extreme_filtered_1



# rm -rf /home/nima/whole_body_tracking/motions/
# mkdir -p /home/nima/whole_body_tracking/motions/
# for csv_file in /home/nima/whole_body_tracking/csvs/*.csv; do
#     python scripts/csv_to_npz.py --input_file "$csv_file" --input_fps 30 --output_name $(basename "$csv_file" .csv) --output_fps 50 --headless
# done