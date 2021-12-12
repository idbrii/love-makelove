import os
from pathlib import Path

from makelove.config import get_config


def load_project(sub_path):
    proj_path = Path(__file__).parent / sub_path
    os.chdir(proj_path.parent)
    return get_config(proj_path)


cfg = load_project("test_projects/duplicates/makelove.toml")
assert cfg["name"] not in ["normalname", "debugname"]
assert cfg["love_version"] not in ["11.0", "11.1"]

cfg = load_project("test_projects/guess_all/makelove.toml")
assert cfg["name"] == "namefromconf"
assert cfg["love_version"] == "11.1"
assert cfg["lovejs"]["title"] == "Title of Window"
