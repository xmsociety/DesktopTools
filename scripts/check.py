import sys
import subprocess

source_dirs = "DesktopTools"
subprocess.check_call(f"isort --check --diff {source_dirs}", shell=True)
subprocess.check_call(f"black --check --diff {source_dirs}", shell=True)
if sys.version_info.major == 3 and sys.version_info.minor != 7:
    subprocess.check_call(
        f"flake8 --ignore W503,E203,E501,E731,F403,F401 {source_dirs} --exclude ui_searchbar.py,searchbar_ui.py,venv/",
        shell=True,
    )
