def execute():
    pass

def console_scripts():
    """ Provides functions which should be converted into executables

    Update this to point to the functions that should be executed as consoles
    scripts. Installing via setup.py will then provide those scripts in your
    environment.

    You can use `./setup.py develop` during development so that the executables
    symlink into your in-development code. Otherwise, they will be installed
    along-side your module with a regular `./setup.py install`.

    """

    return [
        __name__.split('.')[0] + '=' + __name__ + ':' + execute.__name__,
    ]

if __name__ == '__main__':

    # This is necessary so that `python -m` works, but using a function is
    # necessary so that console scripts work. If you don't need console
    # scripts, you can replace this file and write your console script inline,
    # but it shouldn't hurt to keep the current function-based structure
    # either.

    execute()
