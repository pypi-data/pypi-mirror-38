
from setuptools import setup
from stutils import __version__ as version

requirements = [
    line.strip()
    for line in open('requirements.txt')
    if line.strip() and not line.strip().startswith('#')]

# options reference: https://docs.python.org/2/distutils/
# see also: https://packaging.python.org/tutorials/distributing-packages/
setup(
    # whenever you're updating the next three lines
    # please also update oscar.py
    name="strudel.utils",
    version=version,
    author='Marat (@cmu.edu)',
    description="Various utils used internally by strudel.* packages",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[  # full list: https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering'
    ],
    platforms=["Linux", "Solaris", "Mac OS-X", "Unix", "Windows"],
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    packages=['stutils'],
    license="GPL v3.0",
    author_email='marat@cmu.edu',
    url='https://github.com/cmustrudel/strudel.utils',
    install_requires=requirements
)
