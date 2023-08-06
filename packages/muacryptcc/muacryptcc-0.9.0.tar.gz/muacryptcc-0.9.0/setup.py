import os
from setuptools import setup, find_packages

def main():
    with open(os.path.join("muacryptcc", "__init__.py")) as f:
        for line in f:
            if "__version__" in line.strip():
                version = line.split("=", 1)[1].strip().strip('"')
                break

    with open("README.rst") as f:
        long_desc = f.read()

    setup(
        name='muacryptcc',
        description='',
        long_description = long_desc,
        version=version,
        url='https://muacryptcc.readthedocs.io',
        license='MIT license',
        platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
        classifiers=['Development Status :: 3 - Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Utilities',
                     'Intended Audience :: Developers',
                     'Programming Language :: Python'],
        packages=find_packages(),
        entry_points={
            "muacrypt": [
                "muacryptcc=muacryptcc.plugin"
            ]
        },
        install_requires=["muacrypt", "claimchain>=0.3.0"],
        # install_requires=["claimchain", "muacrypt"],
        zip_safe=False,
    )


if __name__ == '__main__':
    main()

