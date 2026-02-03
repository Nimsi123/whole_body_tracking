conda activate beyondmimic

python scripts/rsl_rl/eval.py \
    --task=Tracking-Flat-G1-v0 --num_envs=1 \
    --resume_path /home/nima/whole_body_tracking/genmo_working_examples/2026-01-17_05-22-51_batch_clipped_long_2_wCo9atjANTo_403565_404205_1_2_2_0_0_genmo_gmr_retarget_bm/model_9999.pt \
    --motion_file /home/nima/robot_table_tennis/src/humanoid_mixtape/test_tracking/test_data/batch_clipped_long_2_wCo9atjANTo_403565_404205_1_2_2_0_0_genmo/gmr_retarget_bm.npz