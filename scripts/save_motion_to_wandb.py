import wandb

# COLLECTION = "smplh_ttg_test_1"
COLLECTION = "motive_gameplay_ttg_test_1"

run = wandb.init(project="csv_to_npz", name=COLLECTION)
print(f"[INFO]: Logging motion to wandb: {COLLECTION}")
REGISTRY = "motions"
# logged_artifact = run.log_artifact(artifact_or_path="/home/nima/whole_body_tracking/motions/smplh_ttg_test_1.npz", name=COLLECTION, type=REGISTRY)
logged_artifact = run.log_artifact(artifact_or_path="/home/nima/whole_body_tracking/motions/motive_gameplay_ttg_test_1.npz", name=COLLECTION, type=REGISTRY)
run.link_artifact(artifact=logged_artifact, target_path=f"wandb-registry-{REGISTRY}/{COLLECTION}")
print(f"[INFO]: Motion saved to wandb registry: {REGISTRY}/{COLLECTION}")