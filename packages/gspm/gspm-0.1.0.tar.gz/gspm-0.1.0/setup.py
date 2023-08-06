
import io
import gspm

from setuptools import setup, find_packages


with open('requirements.txt') as reqs_file:
    requirements = reqs_file.read().splitlines()


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md', 'CHANGES')

install_requires = [ 'pyyaml', 'gitpython', 'dotmap', 'wget', 'packaging' ]
test_requires = []

setup(

    name=gspm.__id__,
    copyright=gspm.__copyright__,
    version=gspm.__version__,
    description=gspm.__desc__,
    long_description=long_description,
    url='https://gitlab.com/godot-stuff/gs-project-manager.git',
    author='Paul Hocker',
    author_email='paul@spocker.net',
    license='MIT',
    packages=find_packages('.'),
    package_data={'gspm': 'gspm'},
    install_requires=install_requires,
    zip_safe=True,
    tests_require=test_requires,
    entry_points={
        'console_scripts': ['gspm=gspm.gspm:run'],
    },
    classifiers=[
        # Picked from
        #   http://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Games/Entertainment',
        'Environment :: Console',
    ]
)
