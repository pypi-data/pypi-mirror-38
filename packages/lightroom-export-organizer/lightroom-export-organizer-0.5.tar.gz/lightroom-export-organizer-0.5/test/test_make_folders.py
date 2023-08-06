import os
import shutil
import pytest
import tempfile
from os import path
from collections import defaultdict
from tempfile import NamedTemporaryFile

from lightroom_export_organizer.make_folders import do, undo, validate_file_pairs, read_keyword


@pytest.fixture(scope="function")
def test_fn():
    with tempfile.NamedTemporaryFile('w', delete=False) as fp:
        fp.write("beeb: dest1\n")
    yield fp.name

    if path.isfile(fp.name):
        os.remove(fp.name)

@pytest.fixture(scope="function")
def test_info(tmpdir_factory):

    def touch(fn, keyword):
        with open(fn, 'a') as fp:
            fp.write("beeb: {}\n".format(keyword))

    def make_pair(base_fn, keyword, bad=False):
        touch(base_fn + ".jpg", keyword)
        if not bad:
            touch(base_fn + ".txt", keyword)

    dir_base = str(tmpdir_factory.mktemp("test_dir_base"))
    tmpdir_maker = defaultdict(lambda: path.join(dir_base, str(tmpdir_factory.mktemp("test_dirs"))))

    d1 = path.join(dir_base, "d1")
    os.mkdir(d1)
    make_pair(path.join(d1, "f1"), "dest1")
    make_pair(path.join(d1, "f2"), "dest2")
    make_pair(path.join(d1, "f3"), "dest1", bad=True)

    d2 = path.join(dir_base, "d2")
    os.mkdir(d2)
    make_pair(path.join(d2, "f4"), "dest3")
    make_pair(path.join(d2, "f5"), "dest2", bad=True)

    info = {
        "valid": {
            'f1': (path.join(d1, "f1"), "dest1"),
            'f2': (path.join(d1, "f2"), "dest2"),
            'f4': (path.join(d1, "f4"), "dest3")
        },
        "invalid": {
            'f3': (path.join(d1, "f3"), "dest1"),
            'f5': (path.join(d1, "f5"), "dest2")
        }
    }

    yield dir_base, info

    if path.isdir(dir_base):
        shutil.rmtree(dir_base)
    for dir_name in tmpdir_maker.values():
        if path.isdir(dir_name):
            shutil.rmtree(dir_name)


def test_do(test_info, tmpdir_factory):
    dir_base, info = test_info

    do(dir_base)

    for base_name, (old_path, keyword) in info['valid'].items():
        assert path.isdir(path.join(dir_base, keyword))
        assert path.isfile(path.join(dir_base, keyword, base_name) + ".jpg")
        assert not path.isfile(path.join(dir_base, keyword, base_name) + ".txt")

    for base_name, (old_path, keyword) in info['invalid'].items():
        assert path.isdir(path.join(dir_base, 'unknown'))
        assert path.isfile(path.join(dir_base, 'unknown', base_name) + ".jpg")

    keywords = [e[1] for e in info['valid'].values()]
    dirs_valid = keywords + ['unknown']
    for root, dirs, files in os.walk(dir_base):
        for d in dirs:
            assert d in dirs_valid


def test_read_keyword(test_fn):
    assert "dest1" == read_keyword(test_fn)

    with NamedTemporaryFile(delete=False) as fp:
        fn = fp.name
    keyword = read_keyword(fn)
    os.remove(fn)
    assert keyword is None


def test_validate_file_pairs(test_info):
    test_directory, info = test_info
    valid, invalid = validate_file_pairs(test_directory)

    def get_base_fn(fn):
        return path.splitext(path.basename(fn))[0]

    valid = list(map(get_base_fn, valid))
    invalid = list(map(get_base_fn, invalid))

    for item_valid in info['valid'].keys():
        assert item_valid in valid
        assert item_valid not in invalid

    for item_invalid in info['invalid'].keys():
        assert item_invalid in invalid
        assert item_invalid not in valid
