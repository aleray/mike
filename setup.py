import os
import re
import subprocess
from setuptools import setup, find_packages, Command

from mkultra.app_version import version

root_dir = os.path.abspath(os.path.dirname(__file__))


class Coverage(Command):
    description = 'run tests with code coverage'
    user_options = [
        ('test-suite=', 's',
         "test suite to run (e.g. 'some_module.test_suite')"),
    ]

    def initialize_options(self):
        self.test_suite = None

    def finalize_options(self):
        pass

    def run(self):
        env = dict(os.environ)
        pythonpath = os.path.join(root_dir, 'test', 'scripts')
        if env.get('PYTHONPATH'):
            pythonpath += os.pathsep + env['PYTHONPATH']
        env.update({
            'PYTHONPATH': pythonpath,
            'COVERAGE_FILE': os.path.join(root_dir, '.coverage'),
            'COVERAGE_PROCESS_START': os.path.join(root_dir, '.coveragerc'),
        })

        subprocess.check_call(['coverage', 'erase'])
        subprocess.check_call(
            ['coverage', 'run', 'setup.py', 'test'] +
            (['-q'] if self.verbose == 0 else []) +
            (['-s', self.test_suite] if self.test_suite else []),
            env=env
        )
        subprocess.check_call(['coverage', 'combine'])


custom_cmds = {
    'coverage': Coverage,
}

try:
    from flake8.main.setuptools_command import Flake8

    class LintCommand(Flake8):
        def distribution_files(self):
            return ['setup.py', 'mkultra']

    custom_cmds['lint'] = LintCommand
except ImportError:
    pass

with open(os.path.join(root_dir, 'README.md'), 'r') as f:
    # Read from the file and strip out the badges.
    long_desc = re.sub(r'(^# mkultra)\n\n(.+\n)*', r'\1', f.read())

try:
    import pypandoc
    long_desc = pypandoc.convert(long_desc, 'rst', format='md')
except ImportError:
    pass

setup(
    name='mkultra',
    version=version,

    description=('Manage multiple versions of your MkDocs-powered ' +
                 'documentation'),
    long_description=long_desc,
    keywords='mkdocs multiple versions',
    url='https://github.com/jimporter/mkultra',

    author='Jim Porter',
    author_email='porterj@alum.rit.edu',
    license='BSD',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Topic :: Documentation',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    packages=find_packages(exclude=['test', 'test.*']),

    install_requires=(['mkdocs', 'jinja2', 'packaging', 'ruamel.yaml < 0.15',
                       'six']),
    extras_require={
        'dev': ['coverage', 'flake8 >= 3.0', 'pypandoc'],
        'test': ['coverage', 'flake8 >= 3.0'],
    },

    entry_points={
        'console_scripts': [
            'mkultra=mkultra.driver:main',
        ],
        'mkultra.themes': [
            'mkdocs = mkultra.themes.mkdocs',
            'amelia = mkultra.themes.mkdocs',
            'cerulean = mkultra.themes.mkdocs',
            'cosmo = mkultra.themes.mkdocs',
            'cyborg = mkultra.themes.mkdocs',
            'flatly = mkultra.themes.mkdocs',
            'journal = mkultra.themes.mkdocs',
            'readable = mkultra.themes.mkdocs',
            'simplex = mkultra.themes.mkdocs',
            'slate = mkultra.themes.mkdocs',
            'spacelab = mkultra.themes.mkdocs',
            'united = mkultra.themes.mkdocs',
            'yeti = mkultra.themes.mkdocs',
        ],
    },

    test_suite='test',
    cmdclass=custom_cmds,
    zip_safe=False,
)
