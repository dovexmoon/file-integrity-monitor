import hashlib
import json
import os
from pathlib import Path

BASELINE_FILE = "baseline.json"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)

        return sha256.hexdigest()

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def create_baseline(folder):
    baseline = {}

    for root, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)

            file_hash = calculate_hash(path)

            if file_hash:
                baseline[path] = file_hash

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

    print("Baseline created successfully!")


def monitor(folder):
    try:
        with open(BASELINE_FILE, "r") as f:
            baseline = json.load(f)

    except FileNotFoundError:
        print("Baseline not found. Create one first.")
        return

    current_files = {}

    for root, _, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)

            file_hash = calculate_hash(path)

            if file_hash:
                current_files[path] = file_hash

    for file_path, current_hash in current_files.items():

        if file_path not in baseline:
            print(f"[NEW FILE] {file_path}")

        elif baseline[file_path] != current_hash:
            print(f"[MODIFIED] {file_path}")

    for file_path in baseline:
        if file_path not in current_files:
            print(f"[DELETED] {file_path}")

    print("Monitoring complete.")


def main():
    folder = input("Enter folder path: ")

    if not Path(folder).exists():
        print("Invalid folder path.")
        return

    choice = input(
        "\n1. Create Baseline\n2. Monitor Changes\nChoose option: "
    )

    if choice == "1":
        create_baseline(folder)

    elif choice == "2":
        monitor(folder)

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()