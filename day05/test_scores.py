import os
import tempfile
import show_high_score as shs


def test_sort_dict():
    data = {"Alice": 3, "Bob": 7, "Carl": 1}
    sorted_data = shs.sort_dict(data)
    assert list(sorted_data.keys()) == ["Bob", "Alice", "Carl"]


def test_write_and_read():
    # create temp file
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "high_score.dat")

        # mock filename used in code
        original_path = shs.Path.cwd
        shs.Path.cwd = lambda: tmp

        data = {"Alice": 4, "Bob": 2}
        shs.write(data)

        read_data = shs.read()
        assert read_data == data

        # restore
        shs.Path.cwd = original_path


def test_make_file_creates_empty_file():
    with tempfile.TemporaryDirectory() as tmp:
        original_path = shs.Path.cwd
        shs.Path.cwd = lambda: tmp

        content = shs.make_file()
        assert content == ""

        full_path = os.path.join(tmp, "high_score.dat")
        assert os.path.exists(full_path)

        shs.Path.cwd = original_path
