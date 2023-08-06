from setuptools import setup, find_packages


def read(filename):
    with open(filename, 'r') as f:
        return f.read()


setup(
        name='noted-cli',
        version='0.1.5',
        license='GNU General Public License v2 (GPLv2)',
        description='A VIM-inspired note manager for the console',
        long_description=read('README.md'),
        long_description_content_type='text/markdown',
        author='Johan Kanefur',
        author_email='johan.canefur@gmail.com',
        url='https://bitbucket.org/zappen999/noted-cli',
        platforms='any',
        packages=find_packages(),
        install_requires=read('requirements.txt').splitlines(),
        entry_points={
            'console_scripts': [
                'noted = notedlib.console:tui',
                'noted-cli = notedlib.console:cli'
            ],
        }
)
