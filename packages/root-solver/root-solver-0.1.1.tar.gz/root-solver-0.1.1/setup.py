import setuptools

import versioneer

DESCRIPTION_FILES = ["pypi-intro.rst"]

long_description = []
import codecs
for filename in DESCRIPTION_FILES:
    with codecs.open(filename, 'r', 'utf-8') as f:
        long_description.append(f.read())
long_description = "\n".join(long_description)


setuptools.setup(
    name = "root-solver",
    version = versioneer.get_version(),
    packages = setuptools.find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = [
        "numpy",
    ],
    python_requires = '>=3.4',
    author = "James Tocknell",
    author_email = "aragilar@gmail.com",
    description = "Root solver for polynomial equations",
    long_description = long_description,
    license = "3-clause BSD",
    keywords = "root solver",
    url = "https://root-solver.readthedocs.io",
    project_urls={
        'Documentation': 'https://root-solver.readthedocs.io',
        'Source': 'https://github.com/aragilar/root-solver/',
        'Tracker': 'https://github.com/aragilar/root-solver/issues',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    cmdclass=versioneer.get_cmdclass(),
)
