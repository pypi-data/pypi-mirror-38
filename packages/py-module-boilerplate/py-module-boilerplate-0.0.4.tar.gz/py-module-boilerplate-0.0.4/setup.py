import os
from importlib.machinery import SourceFileLoader
from setuptools import setup, find_packages

module_name = 'py_module_boilerplate'
executable_name = module_name.replace('_', '-')

module = SourceFileLoader(
    module_name,
    os.path.join(module_name, '__init__.py')
).load_module()


def load_requirements(filename):
    """ Load requirements from a pip requirements file """
    with open(filename, 'r') as f:
        for line in map(str.strip, f):
            if line.startswith('#'):
                continue
            if line.startswith('-r '):
                yield from load_requirements(line[3:])
            else:
                yield line


setup(
    name=module_name.replace('_', '-'),
    version=module.__version__,
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    long_description=open('README.rst').read(),
    platforms='all',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: Russian',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=list(load_requirements('requirements.txt')),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            '{0} = {1}.main:main'.format(
                executable_name,
                module_name,
            )
        ],
        'pylama.linter': [
            'imports = flake8_import_order.pylama_linter:Linter',
        ]
    },
    extras_require={
        'develop': list(load_requirements('requirements.dev.txt')),
    },
)
