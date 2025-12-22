# conda activate beyondmimic

# python scripts/rsl_rl/train.py --task=Tracking-Flat-G1-v0 \
# --registry_name ianc-uc-berkeley-org/wandb-registry-motions/smplh_ttg_test_1 \
# --headless --logger wandb --log_project_name ttg --run_name test

# python scripts/rsl_rl/train.py --task=Tracking-Flat-G1-v0 \
# --registry_name ianc-uc-berkeley-org/wandb-registry-motions/7lbDSIKUak_232930_233555_0_1_2_2_original \
# --headless --logger wandb --log_project_name ttg --run_name test_7lbDSIKUak_232930_233555_0_1_2_2_original

# python scripts/rsl_rl/train.py --task=Tracking-Flat-G1-v0 \
# --registry_name ianc-uc-berkeley-org/wandb-registry-motions/motive_repeated_5 \
# --headless --logger wandb --log_project_name ttg --run_name motive_repeated_5

# python scripts/rsl_rl/train.py --task=Tracking-Flat-G1-v0 \
# --registry_name ianc-uc-berkeley-org/wandb-registry-motions/smpl_extreme_2 \
# --headless --logger wandb --log_project_name ttg --run_name smpl_extreme_2

# after SMPL trajectory filtering
python scripts/rsl_rl/train.py --task=Tracking-Flat-G1-v0 \
--registry_name ianc-uc-berkeley-org/wandb-registry-motions/smpl_extreme_filtered_1 \
--headless --logger wandb --log_project_name ttg --run_name smpl_extreme_filtered_1