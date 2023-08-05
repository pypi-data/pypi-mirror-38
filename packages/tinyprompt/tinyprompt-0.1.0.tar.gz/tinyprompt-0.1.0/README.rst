.. image:: https://travis-ci.org/sirosen/tinyprompt.svg?branch=master
    :alt: build status
    :target: https://travis-ci.org/sirosen/tinyprompt

.. image:: https://img.shields.io/pypi/v/tinyprompt.svg
    :alt: Latest Released Version
    :target: https://pypi.org/project/tinyprompt/

.. image:: https://img.shields.io/pypi/pyversions/tinyprompt.svg
    :alt: Supported Python Versions
    :target: https://pypi.org/project/tinyprompt/

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :alt: License
    :target: https://opensource.org/licenses/Apache-2.0


tinyprompt
==========

A tiny lib for nice, handy prompts, primarily for Ops scripts.

This README contains all documentation.

Usage
-----

``pip install tinyprompt``

Use `tinyprompt.skippable` to wrap script steps with a `Yes / Skip / Quit`
prompt. This is very useful for simple scripted operations where
- `yes` is the normal case
- `skip` can be used to resume after a failure or abort
- `quit` is used to abort when issues are encountered

.. code-block:: python

    import tinyprompt

    # note: tinyprompt.skippable passes arguments through verbatim, but it's
    # not guaranteed to return a meaningful result
    # `quit` does a sys.exit(1) and `skip` makes it return `None`

    @tinyprompt.skippable('skippable script step')
    def my_func():
        """
        Do some things, this docstring will show up as a command description
        when the script is run.
        The "skippable script step" arg will be uppercased and used as the step
        name.
        """
        print('this skippable step')


    @tinyprompt.skippable('other skippable script step', color=False)
    def my_func2():
        """another func"""
        print('hi')


    def otherfunc():
        # yes, it's on purpose
        tinyprompt.color_print('red string', tinyprompt.RED)
        tinyprompt.color_print('yellow string', tinyprompt.BLUE)
        tinyprompt.color_print('green string', tinyprompt.GRAY)
        tinyprompt.color_print('blue string', tinyprompt.GREEN)
        tinyprompt.color_print('gray  string', tinyprompt.YELLOW)


    def main():
        my_func()  # skippable
        my_func2()  # skippable
        otherfunc()  # not skippable, but not reached on quit

    if __name__ == '__main__':
        main()


Contributing
------------

- All code must pass `make test`
- All code is autoformatted with `black` and `isort`
- Try to write a test whenever you find a bug
- Make your PRs clean. Rebase to avoid merge conflicts and squash fixup commits
