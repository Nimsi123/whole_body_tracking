#!/bin/bash
#SBATCH --job-name=bm-em4
#SBATCH --partition=Main
#SBATCH --nodelist=em4
#SBATCH --gres=gpu:6
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --qos=low

eval "$(conda shell.bash hook)"

conda activate beyondmimic
cd /home/nima/whole_body_tracking

# Process the videos in that folder
python main.py --gpu_ids 0 1 2 3 4 5 \
                        --workers_per_gpu 2 \
                        --root_dir . \
                        --worker_split 3 \
                        --num_workers 6