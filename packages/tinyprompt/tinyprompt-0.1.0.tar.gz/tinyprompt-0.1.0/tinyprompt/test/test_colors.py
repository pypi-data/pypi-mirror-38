from ..colors import GREEN, RED, color_print


def test_uncolored_output(capsys):
    color_print("foo", None)
    captured = capsys.readouterr()
    assert captured.out == "foo\n"
    assert captured.err == ""


def test_colorized_output(capsys):
    color_print("hello", RED)
    color_print("world", GREEN)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == "\033[0;31mhello\033[0m\n\033[0;32mworld\033[0m\n"
