source ~/.holosoma_deps/miniconda3/bin/activate hssim

# CUDA is required .

# python scripts/parallel_npz_to_csv.py
rm -rf /home/nima/whole_body_tracking/motions/
mkdir -p /home/nima/whole_body_tracking/motions/
for csv_file in /home/nima/whole_body_tracking/csvs/*.csv; do
    python scripts/csv_to_npz.py --input_file "$csv_file" --input_fps 30 --output_name $(basename "$csv_file" .csv) --output_fps 50 --headless
done