import argparse
import os
import subprocess
import glob
from multiprocessing import Process, Queue
import shutil


def is_task_completed(motion_name, logs_dir="/home/nima/whole_body_tracking/logs/rsl_rl/g1_flat"):
    """Check if a task has already been completed by looking for model_29999.pt."""
    if not os.path.exists(logs_dir):
        return False
    
    # Look for any folder ending with _{motion_name} that contains model_29999.pt
    pattern = os.path.join(logs_dir, f"*_{motion_name}", "model_29999.pt")
    matches = glob.glob(pattern)
    return len(matches) > 0


def get_incomplete_run_dir(motion_name, logs_dir="/home/nima/whole_body_tracking/logs/rsl_rl/g1_flat"):
    """Find an incomplete run directory for this motion (has folder but no model_29999.pt)."""
    if not os.path.exists(logs_dir):
        return None
    
    pattern = os.path.join(logs_dir, f"*_{motion_name}")
    matches = glob.glob(pattern)
    
    incomplete_dirs = []
    for match in matches:
        model_path = os.path.join(match, "model_29999.pt")
        if not os.path.exists(model_path):
            incomplete_dirs.append(match)
    
    return incomplete_dirs


def run_task(motion_name, gpu_id):
    """
    Run training for a single motion on a specific GPU.
    """
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
    
    cmd = [
        "python", "scripts/rsl_rl/train.py",
        "--task=Tracking-Flat-G1-v0",
        "--registry_name", "dummy_value",
        "--headless",
        "--logger", "wandb",
        "--log_project_name", "ttg",
        "--run_name", motion_name,
    ]
    
    print(f"[GPU {gpu_id}] Starting training for: {motion_name}")
    result = subprocess.run(
        cmd,
        env=env,
        cwd="/home/nima/whole_body_tracking",
    )
    return result.returncode


def gpu_worker(gpu_id: int, task_queue: Queue):
    """
    Worker process for a specific GPU.
    Repeatedly pops tasks from the queue and runs them.
    """
    while True:
        task = task_queue.get()
        if task is None:  # sentinel → stop
            break
        
        motion_name = task
        
        try:
            returncode = run_task(motion_name, gpu_id)
            if returncode == 0:
                print(f"[GPU {gpu_id}] Completed: {motion_name}")
            else:
                print(f"[GPU {gpu_id}] Failed with code {returncode}: {motion_name}")
        except Exception as e:
            print(f"[GPU {gpu_id}] Task {motion_name} failed: {e}")

    print(f"[GPU {gpu_id}] No more work. Shutting down.")


def discover_tasks(root_dir, num_workers, worker_split, delete_incomplete=False):
    """Discover motion files, filter out completed ones, and split across workers."""
    all_tasks = []
    for file in os.listdir(root_dir):
        if not file.endswith(".npz"):
            continue
        
        motion_name = file[:-4]  # Remove .npz extension
        if is_task_completed(motion_name):
            continue
        if delete_incomplete:
            incomplete_dirs = get_incomplete_run_dir(motion_name)
            for inc_dir in incomplete_dirs:
                print(f"Deleting incomplete run: {inc_dir}")
                shutil.rmtree(inc_dir)
        all_tasks.append(motion_name)

    all_tasks = sorted(all_tasks)
    print(f"Total tasks discovered: {len(all_tasks)}")

    # Split tasks for distributed workers first
    start_idx = int(len(all_tasks) * worker_split / num_workers)
    end_idx = int(len(all_tasks) * (worker_split + 1) / num_workers)
    task_slice = all_tasks[start_idx:end_idx]
    print(f"Tasks for this worker split ({worker_split}/{num_workers}): {len(task_slice)}")

    return task_slice


def main(gpu_ids, workers_per_gpu, num_workers, worker_split):
    """Manage training across GPUs with explicit multiprocessing."""
    
    root_dir = "/home/nima/whole_body_tracking/motions"
    delete_incomplete = (worker_split == 1)
    tasks = discover_tasks(root_dir, num_workers, worker_split, delete_incomplete)
    
    total_workers = len(gpu_ids) * workers_per_gpu

    print(f"GPUs                   : {list(gpu_ids)}")
    print(f"Workers per GPU        : {workers_per_gpu}")
    print(f"Total worker processes : {total_workers}")

    task_queue = Queue()
    for t in tasks:
        task_queue.put(t)
    # Add sentinel values to signal workers to stop
    for _ in range(total_workers):
        task_queue.put(None)

    processes = []
    for gpu in gpu_ids:
        for _ in range(workers_per_gpu):
            p = Process(target=gpu_worker, args=(gpu, task_queue))
            p.start()
            processes.append(p)

    for p in processes:
        p.join()
    
    print("All tasks completed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run parallel training across GPUs")
    parser.add_argument("--root_dir", default="/home/nima/whole_body_tracking/motions",
                        help="Root directory containing motion .npz files")
    parser.add_argument("--gpu_ids", nargs='+', type=int, default=None,
                        help="List of GPU IDs to use (e.g., --gpu_ids 0 1 2)")
    parser.add_argument("--workers_per_gpu", type=int, default=2,
                        help="Number of worker processes per GPU")
    parser.add_argument("--num_workers", type=int, default=1,
                        help="Total number of distributed worker machines (for splitting work)")
    parser.add_argument("--worker_split", type=int, default=0,
                        help="This worker's index (0 to num_workers-1)")
    args = parser.parse_args()
    
    main(args.gpu_ids, args.workers_per_gpu, args.num_workers, args.worker_split)
