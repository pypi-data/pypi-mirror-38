import pytest
from pathlib import Path
from difflib import ndiff
from dover import project


def test_toml_find_config_file(toml_files):
    cfg_file = project.find_config_file(cwd=toml_files.temp_dir)
    assert cfg_file is not None
    assert cfg_file.name == "pyproject.toml"


def test_toml_collect_versioned_files(toml_files):

    cfg_file = project.find_config_file(cwd=toml_files.temp_dir)
    versioned_files = project.collect_versioned_files(cfg_file)

    assert len(versioned_files) == 3
    assert versioned_files[0].name == "pyproject.toml"
    assert versioned_files[1].name == "cli.py"
    assert versioned_files[2].name == "README.md"


def test_toml_collect_versioned_files_failure(tmpdir):
    cfg_file = Path(tmpdir, "pyproject.toml")
    with cfg_file.open("w") as fh_:
        fh_.write('\n\n[tool.dover]\nversioned_files = ["somefile.txt"]')

    with pytest.raises(project.ConfigurationError) as ex_info:
        project.collect_versioned_files(cfg_file)

    err_msg = "Invalid versioned file reference. Path does not exist: somefile.txt"
    assert ex_info.value.args[0] == err_msg


def test_toml_no_dover_entry(toml_files):
    with toml_files.pyproject_toml.open("r") as fh_:
        content = fh_.read()
    with toml_files.pyproject_toml.open("w") as fh_:
        fh_.write(content.replace("[tool.dover]\n", ""))

    with pytest.raises(project.ConfigurationError) as ex_info:
        project.collect_versioned_files(toml_files.pyproject_toml)

    err_msg = "Could not read dover section from pyproject.toml"
    assert ex_info.value.args[0] == err_msg


variations = [
    ("0.2", "v0.2"),
    ("0.2", "version = 0.2"),
    ("0.2", "__version__ = 0.2"),
    ("0.2", "    version = 0.2    \n"),
    ("0.2", "    __version__ = 0.2   \n"),
    ("0.2", "version = '0.2'"),
    ("0.2", 'version = "0.2"'),
    ("0.2", "version 0.2"),
    ("0.2", "__version__ = '0.2'"),
    ("0.2", '__version__ = "0.2"'),
    ("0.3.0", "version = 0.3.0"),
    ("0.3.0", "version = 0.3.0 \n"),
    ("0.3.0", "version 0.3.0 \n"),
    (
        "0.2.4",
        '![version-badge](https://img.shields.io/badge/version-v0.2.4-green.svg "v0.2.4")',
    ),
]


@pytest.fixture(params=variations)
def test_toml_version_regex(request):
    expected, version_match = request.param
    rx = project.version_regex()
    m = rx(version_match)
    assert m is not None
    assert m.groupdict()["version"] == expected


FILE_SAMPLE = ["import os", "__version__ = '0.1.0'", "", "value = 1"]


@pytest.fixture
def sample():
    vfile = project.VersionedFile()
    vfile.content = FILE_SAMPLE
    vfile.collect_version_info()
    yield vfile


def test_toml_versionfile_collect_version_info(sample):
    assert len(sample.versioned_lines) == 1


def test_toml_assert_versions_failure(toml_files):

    config = project.find_config_file(cwd=toml_files.temp_dir)
    vfiles = project.collect_versioned_files(config)

    # insert additional bogus version number
    vfiles[0].versioned_lines.append((99, "version = '2.6.1'", "2.6.1"))

    print(vfiles[0].versioned_lines)

    with pytest.raises(project.VersionMissMatchError) as ex_info:
        project.assert_versions(vfiles)

    assert ex_info.value.args[0] == (
        "Not all file versions match:\n\n"
        '    pyproject.toml 0.3.0 (version = "0.3.0")     \n'
        "    pyproject.toml 2.6.1 (version = '2.6.1')     \n"
        "    newd/cli.py    0.3.0 (__version__ = '0.3.0') \n"
        "    README.md      0.3.0 (#### newd app v0.3.0)  "
    )


def test_toml_print_versioned_lines(toml_files, capsys):
    config = project.find_config_file(cwd=toml_files.temp_dir)
    vfiles = project.collect_versioned_files(config)

    project.print_versioned_lines(vfiles)

    captured = capsys.readouterr()

    assert captured.out == (
        '    pyproject.toml 0002 (version = "0.3.0")     \n'
        "    newd/cli.py    0002 (__version__ = '0.3.0') \n"
        "    README.md      0000 (#### newd app v0.3.0)  \n"
    )


def test_toml_print_versioned_updates(toml_files, capsys):

    config = project.find_config_file(cwd=toml_files.temp_dir)
    vfiles = project.collect_versioned_files(config)

    project.print_versioned_updates(vfiles, "0.4.0")

    captured = capsys.readouterr()

    assert captured.out == (
        "    pyproject.toml (0.3.0 -> 0.4.0)\n"
        "    newd/cli.py    (0.3.0 -> 0.4.0)\n"
        "    README.md      (0.3.0 -> 0.4.0)\n"
    )


def test_toml_versionedfile_update(toml_files):

    config = project.find_config_file(cwd=toml_files.temp_dir)
    vfiles = project.collect_versioned_files(config)

    vfiles[0].update("0.4.0")
    assert vfiles[0].content[2] == 'version = "0.4.0"\n'

    vfiles[1].update("0.4.0")
    assert vfiles[1].content[2] == "__version__ = '0.4.0'\n"

    vfiles[2].update("0.4.0")
    assert vfiles[2].content[0] == "#### newd app v0.4.0\n"


def do_diff(a, b):
    diff = ndiff(a, b)
    lines = [line for line in diff if line[0] in ("+", "-")]
    return "".join(lines)


def compare_save_diff(vfile, src_content, diff_string):

    print("comparing {}".format(vfile.name))

    vfile.update("0.4.0")
    vfile.save()

    with vfile.file_path.open("r") as fh_:
        org_content = src_content.splitlines(keepends=True)
        new_content = fh_.read().splitlines(keepends=True)
        diff = do_diff(org_content, new_content)
        assert diff == diff_string


def test_toml_versionedfile_save(toml_files):

    config = project.find_config_file(cwd=toml_files.temp_dir)
    vfiles = project.collect_versioned_files(config)

    compare_save_diff(
        vfiles[0],
        toml_files.pyproject_toml_content,
        '- version = "0.3.0"\n+ version = "0.4.0"\n',
    )

    compare_save_diff(
        vfiles[1],
        toml_files.cli_py_content,
        "- __version__ = '0.3.0'\n+ __version__ = '0.4.0'\n",
    )

    compare_save_diff(
        vfiles[2],
        toml_files.readme_content,
        "- #### newd app v0.3.0\n+ #### newd app v0.4.0\n",
    )
