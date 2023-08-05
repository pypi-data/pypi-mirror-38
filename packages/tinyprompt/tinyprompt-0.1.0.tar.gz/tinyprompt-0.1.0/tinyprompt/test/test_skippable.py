import io

import pytest

from ..skippable_prompt import skippable


def test_quit(capsys, monkeypatch):
    """q/quit triggers SystemExit"""

    @skippable("run step title")
    def simple_command():
        print("hi")

    monkeypatch.setattr("sys.stdin", io.StringIO("q\n"))
    with pytest.raises(SystemExit):
        simple_command()
    monkeypatch.setattr("sys.stdin", io.StringIO("quit\n"))
    with pytest.raises(SystemExit):
        simple_command()


def test_run_step(capsys, monkeypatch):
    """running a skippable step prints the docstring, runs the method body, etc"""

    @skippable("stepname")
    def mystep():
        """run stepname! hooray!"""
        print("inner activity")

    monkeypatch.setattr("sys.stdin", io.StringIO("y\n"))
    mystep()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert "Step: STEPNAME" in captured.out
    assert "run stepname! hooray!" in captured.out
    assert "Run this?" in captured.out
    assert "inner activity" in captured.out


def test_bad_answer_reprompt(capsys, monkeypatch):
    """test that entering a bad answer results in a reprompt"""

    @skippable("stepname")
    def mystep():
        print("inner activity")

    monkeypatch.setattr("sys.stdin", io.StringIO("wut\nyes\n"))
    mystep()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert "Step: STEPNAME" in captured.out
    assert "Run this?" in captured.out
    assert 'Could not handle "wut". Please answer one of' in captured.out
    assert "inner activity" in captured.out


def test_skip(capsys, monkeypatch):
    """skipping results in no-op, but prompts still print"""

    @skippable("stepname")
    def mystep():
        print("inner activity")

    monkeypatch.setattr("sys.stdin", io.StringIO("s\n"))
    mystep()
    captured = capsys.readouterr()
    assert captured.err == ""
    assert "Step: STEPNAME" in captured.out
    assert "Run this?" in captured.out
    assert "inner activity" not in captured.out
