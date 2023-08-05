import setuptools

import mercy as project
from mercy import __main__


if int(setuptools.__version__.split('.', 1)[0]) < 38:
    raise EnvironmentError(
        'Please upgrade setuptools. This package uses setup.cfg, which requires '
        'setuptools version 38 or higher. If you use pip, for instance, you can '
        'upgrade easily with ` pip install -U setuptools `'
    )


setuptools.setup(
    description=project.short_description(),
    long_description=project.long_description(),
    name=project.name(),
    version=project.version_string(),

    entry_points={
        'console_scripts': getattr(__main__, 'console_scripts', list)(),
    }
)
