from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='py_co_commit',
    version='0.1',
    description='An easy way to create a commit with multiple authors',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/vincentdnl/py-co-commit.git',
    author='Vincent Déniel',
    author_email='vincentdnl@users.noreply.github.com',
    license='apache-2.0',
    packages=['py_co_commit'],
    entry_points={
        'console_scripts': ['py_co_commit=py_co_commit:main'],
    }
)
