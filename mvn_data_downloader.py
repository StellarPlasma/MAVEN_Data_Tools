"""
This module provides functions for downloading Maven data from the Berkeley or LASP servers.
"""

import argparse
import os
import re
import subprocess
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# === CONFIGURATION ===
# Define BASE_URL. Base URL for Maven data can either be the Berkeley or the LASP URL.
BASE_URL = "https://sprg.ssl.berkeley.edu/data/maven/data/sci/"
# BASE_URL = "https://lasp.colorado.edu/maven/sdc/public/data/sci/"
LOCAL_ROOT = "D:/Planetary/data/maven/data/sci/"  # The local root directory for storing downloaded files.
WGET_PATH = r"C:\\Users\\local-user\\wget.exe"  # Path to the wget executable.
USER_AGENT = {"User-Agent": "Mozilla/5.0"}
VALID_EXTENSIONS = (".sav", ".cdf", ".asc", ".txt")

# Define SPECIAL_CASES for instruments that have special cases.
SPECIAL_CASES = {
    "mag": ["l2/sav/1sec", "l2/sav/30sec", "l2/sav/full"],
    "sep": ["l2", "l3/pad/sav"],
    "euv": ["l2", "l3"],
    "sta": ["l2", "l3/cio", "l3/density", "l3/temperature"],
}


# === UTILITY FUNCTIONS ===
def generate_months(start: str, end: str):
    months = []
    start_date = datetime.strptime(start, "%Y-%m")
    end_date = datetime.strptime(end, "%Y-%m")
    while start_date <= end_date:
        months.append((start_date.year, start_date.month))
        start_date += timedelta(days=32)
        start_date = start_date.replace(day=1)
    return months


def get_target_dirs(instrument: str):
    if instrument in SPECIAL_CASES:
        return SPECIAL_CASES[instrument]
    return ["l2", "ql"]


def list_remote_files(url):
    try:
        resp = requests.get(url, headers=USER_AGENT, timeout=15)
        if resp.status_code in (401, 403):
            return "auth", []
        soup = BeautifulSoup(resp.text, "html.parser")
        files = [
            a.get("href")
            for a in soup.find_all("a")
            if a.get("href", "").endswith(VALID_EXTENSIONS)
        ]
        return "ok", files
    except Exception as e:
        return "error", str(e)


def download_file(url, path, dry_run):
    if os.path.exists(path):
        return "[SKIP] Already exists"
    if dry_run:
        return f"[DRY-RUN] Would download {url}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    result = subprocess.run(
        [
            WGET_PATH,
            "--no-check-certificate",
            "--progress=bar:force:noscroll",
            "-O",
            path,
            url,
        ]
    )
    if result.returncode != 0:
        return f"[FAIL] Download failed: {url}"
    return f"[OK] Downloaded: {os.path.basename(path)}"


def sync(instrument: str, start: str, end: str, dry_run: bool):
    target_dirs = get_target_dirs(instrument)
    months = generate_months(start, end)

    for subdir in target_dirs:
        for year, month in months:
            remote_url = (
                f"{BASE_URL}{instrument}/{subdir}/{year}/{str(month).zfill(2)}/"
            )
            local_path = os.path.join(
                LOCAL_ROOT, instrument, subdir, str(year), str(month).zfill(2)
            )
            print(f"\n[CHECK] {remote_url}")

            status, files = list_remote_files(remote_url)
            if status == "auth":
                print("  [SKIP] Login required.")
                continue
            elif status == "error":
                print(f"  [ERROR] {files}")
                continue

            for file in tqdm(files, desc=f"Downloading files", unit="file"):
                file_url = urljoin(remote_url, file)
                file_path = os.path.join(local_path, file)
                msg = download_file(file_url, file_path, dry_run)
                tqdm.write(" " + msg)


if __name__ == "__main__":
    # MAVEN data are organized as follows:
    # ├─ data/
    # │  ├─ maven/
    # │  │  ├─ data/
    # │  │  │  ├─ sci/
    # │  │  │  │  ├─ iuv/
    # │  │  │  │  ├─ kp/
    # │  │  │  │  ├─ lpw/
    # │  │  │  │  ├─ mag/
    # │  │  │  │  ├─ ngi/
    # │  │  │  │  ├─ sep/
    # │  │  │  │  ├─ sta/
    # │  │  │  │  ├─ swe/
    # │  │  │  │  ├─ swi/
    # │  │  │  │  ├─ euv/
    # │  │  │  │  ├─ acc/
    instrument = "swe"  # Specify the instrument here
    start = "2014-10"  # Specify the start date here
    end = "2026-01"  # Specify the end date here
    dry_run = False  # Set to False to download directly, or True to simulate download

    sync(instrument, start, end, dry_run)
