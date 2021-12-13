import os
from pathlib import Path

from makelove.config import get_config

toml = """
default_targets = [
    "win32",
]
build_directory = "build"

love_files = [
    "::git-ls-tree::",
    "-*/.*",
]

[lovejs]
"""

test_project = Path(__file__).parent / "test_project"
makelove_path = test_project / "makelove.toml"


def load_project(conf_name, conf_text):
    conf = test_project / conf_name
    with conf.open("w") as f:
        f.write(conf_text)
    cfg = get_config(makelove_path)
    conf.unlink()
    return cfg


def setup_module(module):
    test_project.mkdir(exist_ok=True)
    os.chdir(test_project)
    with makelove_path.open("w") as f:
        f.write(toml)


def teardown_module(module):
    makelove_path.unlink()
    os.chdir(test_project.parent)
    test_project.rmdir()


def test_all_guessables():
    cfg = load_project(
        "conf.lua",
        """
function love.conf(t)
    t.identity     = 'namefromconf'
    t.version      = '11.1'
    t.window.title = 'Title of Window'
end""",
    )
    assert cfg["name"] == "namefromconf"
    assert cfg["love_version"] == "11.1"
    assert cfg["lovejs"]["title"] == "Title of Window"


def test_duplicates():
    cfg = load_project(
        "conf.lua",
        """
function love.conf(t)
    if true then
        t.identity     = 'normalname'
        t.version      = '11.0'
        t.window.title = 'Title of Window'
    else
        t.identity     = 'debugname'
        t.version      = '11.1'
        t.window.title = 'Debug Window'
    end
end
    """,
    )
    assert cfg["name"] not in ["normalname", "debugname"]
    assert cfg["love_version"] not in ["11.0", "11.1"]


def test_comments():
    cfg = load_project(
        "conf.lua",
        """
function love.conf(t)
    --t.identity     = 'namefromconf'
    -- t.version      = '11.1'
    -- OLD title: t.window.title = 'Title of Window'
end""",
    )
    assert cfg["name"] != "namefromconf"
    assert cfg["love_version"] != "11.1"
    assert "title" not in cfg["lovejs"]
