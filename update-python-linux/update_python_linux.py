import sys
import urllib.request
import re
import subprocess
import os
from pathlib import Path
import gzip
from io import BytesIO
from datetime import datetime

def local_print(output):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    border = "-" * 40
    print(border)
    print(f"[{timestamp}] {output}")
    print(border)

def get_current_version():
    return sys.version.split()[0]

def get_latest_python_version():
    url = "https://www.python.org/downloads/"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": "gzip"
        }
    )

    with urllib.request.urlopen(req) as response:
        encoding = response.info().get("Content-Encoding")

        if encoding == "gzip":
            buf = BytesIO(response.read())
            with gzip.GzipFile(fileobj=buf) as f:
                html = f.read().decode("utf-8")
        else:
            html = response.read().decode("utf-8")

    match = re.search(r'href="/downloads/release/python-\d+[^"]*">Python (3\.\d+\.\d+)</a>', html)
    if match:
        local_print(f"[DONE] Found latest version: {match.group(1)}")
        return match.group(1)

    local_print("[ERROR] Regex failed to find latest version.")
    return None

def run_command(command, cwd=None):
    local_print(f"[RUN] Running: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        local_print(f"[ERROR] Command failed: {command}")
        sys.exit(1)

def install_dependencies():
    local_print("[DEPENDENCIES] Installing build dependencies...")
    run_command("sudo apt update")
    run_command("sudo apt install -y make build-essential libssl-dev zlib1g-dev "
                "libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm "
                "libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev")

def download_and_install(latest_version):
    home = str(Path.home())
    src_dir = os.path.join(home, "python-src")
    os.makedirs(src_dir, exist_ok=True)

    tgz_url = f"https://www.python.org/ftp/python/{latest_version}/Python-{latest_version}.tgz"
    tgz_path = os.path.join(src_dir, f"Python-{latest_version}.tgz")

    local_print(f"[DOWNLOAD] Downloading Python {latest_version} source...")
    run_command(f"wget {tgz_url} -O {tgz_path}")

    local_print("[EXTRACT] Extracting source...")
    run_command(f"tar -xvf Python-{latest_version}.tgz", cwd=src_dir)

    build_dir = os.path.join(src_dir, f"Python-{latest_version}")
    local_print("[CONFIGURE] Configuring build...")
    run_command("./configure --enable-optimizations", cwd=build_dir)

    local_print("[BUILD] Building Python (this may take a while)...")
    run_command("make -j1", cwd=build_dir)  # safer on low RAM devices

    local_print("[INSTALL] Installing Python...")
    run_command("sudo make altinstall", cwd=build_dir)

    short_version = ".".join(latest_version.split(".")[:2])
    python_bin = f"/usr/local/bin/python{short_version}"

    local_print("[VENV] Creating virtual environment...")
    venv_path = os.path.join(home, f"venv-py{short_version}")
    run_command(f"{python_bin} -m venv {venv_path}")

    local_print(f"[DONE] Python {latest_version} installed at {python_bin}")
    local_print(f"[DONE] Virtual environment created at {venv_path}")
    local_print(f"[TIP] To activate it, run:\n\n  source {venv_path}/bin/activate\n")

def main():
    current_version = get_current_version()
    local_print(f"[PYTHON] Current Python version: {current_version}")

    latest_version = get_latest_python_version()
    if not latest_version:
        local_print("[ERROR] Unable to retrieve latest Python version.")
        return

    if current_version != latest_version:
        local_print(f"[UPDATE] Newer version {latest_version} available.")
        install_dependencies()
        download_and_install(latest_version)
    else:
        local_print("[INFO] Python is already up to date.")

if __name__ == "__main__":
    main()
