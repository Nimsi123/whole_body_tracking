#!/usr/bin/env bash
set -euo pipefail

# --------------------------
# User config
# --------------------------
ROOT="/home/nima/whole_body_tracking/logs/rsl_rl/g1_flat"
PATTERN="2025-12-22_21*_original"
MOTIONS_DIR="/home/nima/whole_body_tracking/motions"
VIDEO_LENGTH=200                 # video length in steps (IsaacLab)
TASK="Tracking-Flat-G1-v0"       # IsaacLab task name
NUM_ENVS=2

PLAY_SCRIPT="/home/nima/whole_body_tracking/scripts/rsl_rl/play.py"
OUTDIR="$HOME/whole_body_tracking/isaaclab_sweep_videos_$(date +%Y%m%d_%H%M%S)"
CLIPDIR="$OUTDIR/clips"

mkdir -p "$CLIPDIR"
CLIP_LIST="$OUTDIR/concat_list.txt"
: > "$CLIP_LIST"

# --------------------------
# Dependencies sanity checks
# --------------------------
need_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1"; exit 1; }; }
need_cmd ffmpeg

# --------------------------
# Folder discovery (safe + sorted)
# --------------------------
mapfile -t FOLDERS < <(find "$ROOT" -maxdepth 1 -type d -name "$PATTERN" | sort)
echo "Found ${#FOLDERS[@]} folders."
if [[ ${#FOLDERS[@]} -eq 0 ]]; then
  echo "No folders matched: $ROOT/$PATTERN"
  exit 1
fi

# --------------------------
# Helpers
# --------------------------
# Extract motion name from folder name (everything after YYYY-MM-DD_HH-MM-SS_)
get_motion_name() {
  local folder_name="$1"
  # Folder name format: 2025-12-23_15-42-29_motion_name_here
  # Extract everything after the datetime prefix
  echo "$folder_name" | sed -E 's/^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}_//'
}

# Find highest-indexed .pt file in a directory
get_highest_pt_file() {
  local dir="$1"
  # List all model_*.pt files, extract the number, sort numerically, pick highest
  ls -1 "$dir"/model_*.pt 2>/dev/null | \
    sed -E 's/.*model_([0-9]+)\.pt/\1 &/' | \
    sort -n -k1 | \
    tail -n 1 | \
    awk '{print $2}'
}

# --------------------------
# Main loop
# --------------------------
for i in "${!FOLDERS[@]}"; do
  folder="${FOLDERS[$i]}"
  idx=$((i+1))
  folder_name="$(basename "$folder")"

  # Find highest-indexed .pt file
  resume_path="$(get_highest_pt_file "$folder")"
  if [[ -z "${resume_path:-}" ]]; then
    echo "[$idx/${#FOLDERS[@]}] Skipping (no model_*.pt): $folder"
    continue
  fi

  # Extract motion name from folder name and construct motion file path
  motion_name="$(get_motion_name "$folder_name")"
  motion_file="$MOTIONS_DIR/${motion_name}.npz"

  if [[ ! -f "$motion_file" ]]; then
    echo "[$idx/${#FOLDERS[@]}] Skipping (motion file not found): $motion_file"
    continue
  fi

  echo "[$idx/${#FOLDERS[@]}] Processing: $folder"
  echo "  - Resume path: $resume_path"
  echo "  - Motion file: $motion_file"

  # Run IsaacLab play.py with video recording
  # The video will be saved to the log directory's videos/play folder
  python "$PLAY_SCRIPT" \
    --task "$TASK" \
    --num_envs "$NUM_ENVS" \
    --resume_path "$resume_path" \
    --motion_file "$motion_file" \
    --video \
    --video_length "$VIDEO_LENGTH" \
    --headless

  # Find the recorded video and copy it to our clips directory
  video_src_dir="$(dirname "$resume_path")/videos/play"
  latest_video="$(ls -1t "$video_src_dir"/*.mp4 2>/dev/null | head -n 1 || true)"
  
  if [[ -n "${latest_video:-}" ]]; then
    clip="$CLIPDIR/$(printf "%03d" "$idx")_${motion_name}.mp4"
    cp "$latest_video" "$clip"
    printf "file '%s'\n" "$clip" >> "$CLIP_LIST"
    echo "  - Saved clip: $clip"
  else
    echo "  ! Warning: No video found in $video_src_dir"
  fi

  echo ""
done

# --------------------------
# Concatenate
# --------------------------
if [[ -s "$CLIP_LIST" ]]; then
  FINAL="$OUTDIR/isaaclab_sweep_concat.mp4"
  echo "Concatenating clips into: $FINAL"

  ffmpeg -y -hide_banner -loglevel error \
    -f concat -safe 0 -i "$CLIP_LIST" \
    -c copy \
    "$FINAL"

  echo "Done."
  echo "Output folder: $OUTDIR"
  echo "Final video:   $FINAL"
else
  echo "No clips were recorded. Nothing to concatenate."
fi
