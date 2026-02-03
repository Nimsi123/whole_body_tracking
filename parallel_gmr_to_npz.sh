conda activate gmr

# Pipeline: GMR .pkl -> CSV -> NPZ for BeyondMimic
#
# This script:
# 1. Converts GMR's retargeted .pkl files to CSV format
# 2. Runs csv_to_npz.py sequentially to create NPZ files for BeyondMimic training
#
# Usage:
#   ./parallel_gmr_to_npz.sh [INPUT_PKL_DIR]
#
# Example:
#   ./parallel_gmr_to_npz.sh ~/GMR/retargeted_demo_data/tt4d_mixtape_genmo

set -e

# Configuration
INPUT_PKL_DIR="${1:-$HOME/GMR/retargeted_demo_data/tt4d_mixtape_genmo}"
INPUT_FPS=30  # GMR outputs at 30 FPS
OUTPUT_FPS=50  # BeyondMimic expects 50 FPS

# Derived paths
CSV_DIR="$HOME/whole_body_tracking/csvs/gmr_converted"
MOTIONS_DIR="$HOME/whole_body_tracking/motions"
SCRIPT_DIR="$HOME/whole_body_tracking/scripts"

echo "=========================================="
echo "GMR -> BeyondMimic Pipeline"
echo "=========================================="
echo "Input PKL dir: $INPUT_PKL_DIR"
echo "CSV output dir: $CSV_DIR"
echo "NPZ output dir: $MOTIONS_DIR"
echo "Input FPS: $INPUT_FPS -> Output FPS: $OUTPUT_FPS"
echo "=========================================="

# Create output directories
mkdir -p "$CSV_DIR"
mkdir -p "$MOTIONS_DIR"

# Step 1: Convert all PKL files to CSV (fast, single-threaded is fine)
echo ""
echo "[Step 1/2] Converting PKL files to CSV..."
python "$SCRIPT_DIR/pkl_to_csv.py" \
    --input_dir "$INPUT_PKL_DIR" \
    --output_dir "$CSV_DIR"

source ~/.holosoma_deps/miniconda3/bin/activate hssim


# Step 2: Convert CSV to NPZ sequentially using Isaac Sim
echo ""
echo "[Step 2/2] Converting CSV files to NPZ..."

for csv_file in "$CSV_DIR"/*.csv; do
    [ -e "$csv_file" ] || continue
    
    # Get the motion name (filename without .csv, add _original suffix for consistency)
    filename=$(basename "$csv_file")
    motion_name="${filename%.csv}_original"
    
    echo "Processing: $motion_name"
    
    python "$SCRIPT_DIR/csv_to_npz.py" \
        --input_file "$csv_file" \
        --input_fps "$INPUT_FPS" \
        --output_name "$motion_name" \
        --output_fps "$OUTPUT_FPS" \
        --headless
done

# Summary
echo ""
echo "=========================================="
echo "Pipeline Complete!"
echo "=========================================="
echo "NPZ files saved to: $MOTIONS_DIR"
echo ""
echo "Next steps:"
echo "  1. Run BeyondMimic training:"
echo "     python main.py --gpu_ids 0 1 2 3 --workers_per_gpu 1"
echo ""
echo "  2. Or train a single motion:"
echo "     python scripts/rsl_rl/train.py --task=Tracking-Flat-G1-v0 \\"
echo "         --registry_name dummy_value --headless \\"
echo "         --logger wandb --log_project_name ttg --run_name <motion_name>"
echo "=========================================="

