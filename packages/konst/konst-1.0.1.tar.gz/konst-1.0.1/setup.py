import os

from setuptools import find_packages, setup

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def _open(*path):
    return open(os.path.join(PROJECT_DIR, *path))


def _read_version():
    with _open('konst', '__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip().strip('\'')


def _read(*path):
    with _open(*path) as f:
        return f.read()


def main():
    setup(
        name='konst',
        version=_read_version(),
        description='Effortless, meaningless, DRY constants',
        long_description=_read('README.rst'),
        packages=find_packages(exclude=['tests']),
        python_requires=">=3.6",
        extras_require={
            'dev': ['isort', 'black', 'pytest', 'pytest-watch', 'pytest-cov']
        },
        url='https://github.com/yehonatanz/konst',
        classifiers=(
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ),
    )


if __name__ == '__main__':
    main()
