from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

version = __import__('htg').VERSION

setup(
    name='htg',
    version=version,
    author='R Meurders',
    author_email='pypi+htg@rmnl.net',
    license='MIT',
    description='Happy Tree Gallery is a command line utility generating '
                'static photo galleries.',
    long_description=long_description,
    keywords='development command line tool photos pictures management '
             'galleries json',
    url='https://gitlab.com/rmnl/htg',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click>=7.0,<=7.999',
        'markdown2>=2.3.6,<=2.3.999',
        'numpy>=1.15.2,<=1.15.999',
        'peewee>=3.7.1,<=3.7.999',
        'Pillow>=5.3.0,<=5.3.999',
        'PyYAML>=3.13,<=3.999',
    ],
    entry_points={
        'console_scripts': [
            'htg = htg.__main__:main'
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)
